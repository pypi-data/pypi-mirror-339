"""
ASR Processor module that implements automatic speech recognition using MLX models.

This module provides speech-to-text functionality with MLX-optimized Whisper models
as the primary engine, with CoreML fallbacks for specific situations.
"""

import logging
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

# Conditional imports for different backends
try:
    import mlx.core as mx
    import mlx_whisper

    HAS_MLX = True
except ImportError:
    HAS_MLX = False

try:
    import coremltools as ct

    HAS_COREML = True
except ImportError:
    HAS_COREML = False

from llama_voice.models.coreml_fallback import load_coreml_model
from llama_voice.utils.audio import AudioSegment
from llama_voice.utils.logging import setup_logger


class ASRModelType(Enum):
    """Types of ASR models supported by the processor."""

    MLX_WHISPER_TINY = "mlx-whisper-tiny"
    MLX_WHISPER_BASE = "mlx-whisper-base"
    MLX_WHISPER_SMALL = "mlx-whisper-small"
    MLX_WHISPER_MEDIUM = "mlx-whisper-medium"
    MLX_WHISPER_LARGE = "mlx-whisper-large"
    MLX_WHISPER_LARGE_V2 = "mlx-whisper-large-v2"
    MLX_WHISPER_LARGE_V3 = "mlx-whisper-large-v3"
    MLX_WHISPER_TURBO = "mlx-whisper-turbo"
    COREML_WHISPER = "coreml-whisper"
    CUSTOM = "custom"


@dataclass
class TranscriptionOptions:
    """Configuration options for transcription."""

    language: Optional[str] = None
    task: str = "transcribe"
    beam_size: int = 5
    best_of: int = 1
    temperature: float = 0.0
    patience: float = 1.0
    length_penalty: float = 1.0
    suppress_tokens: List[int] = None
    initial_prompt: Optional[str] = None
    word_timestamps: bool = False
    prepend_punctuations: str = "'¿([{-"
    append_punctuations: str = "'.。,，!！?？:：)]}、"


class ASRProcessor:
    """
    ASR Processor that provides speech-to-text functionality.

    This class implements automatic speech recognition using MLX-optimized
    Whisper models as the primary engine, with CoreML fallbacks for specific
    situations. It handles loading models, processing audio, and returning
    transcriptions with confidence scores.
    """

    # Model URLs for automatic downloading
    MODEL_URLS = {
        ASRModelType.MLX_WHISPER_TINY: "https://huggingface.co/mlx-community/whisper-tiny-mlx/resolve/main/whisper-tiny-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_BASE: "https://huggingface.co/mlx-community/whisper-base-mlx/resolve/main/whisper-base-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_SMALL: "https://huggingface.co/mlx-community/whisper-small-mlx/resolve/main/whisper-small-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_MEDIUM: "https://huggingface.co/mlx-community/whisper-medium-mlx/resolve/main/whisper-medium-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_LARGE: "https://huggingface.co/mlx-community/whisper-large-mlx/resolve/main/whisper-large-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_LARGE_V2: "https://huggingface.co/mlx-community/whisper-large-v2-mlx/resolve/main/whisper-large-v2-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_LARGE_V3: "https://huggingface.co/mlx-community/whisper-large-v3-mlx/resolve/main/whisper-large-v3-mlx.tar.gz",
        ASRModelType.MLX_WHISPER_TURBO: "https://huggingface.co/mlx-community/whisper-turbo-mlx/resolve/main/whisper-turbo-mlx.tar.gz",
    }

    def __init__(
        self,
        model_name: Union[str, ASRModelType] = ASRModelType.MLX_WHISPER_MEDIUM,
        model_path: Optional[str] = None,
        use_mlx: bool = True,
        fallback_to_coreml: bool = True,
        language: Optional[str] = None,
        beam_size: int = 5,
        cache_dir: Optional[Union[str, Path]] = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the ASR processor.

        Args:
            model_name: Name or type of the ASR model to use
            model_path: Path to a custom model (if model_type is CUSTOM)
            use_mlx: Whether to use MLX for model inference
            fallback_to_coreml: Whether to fall back to CoreML if MLX is not available
            language: Default language for transcription
            beam_size: Beam size for decoding
            cache_dir: Directory to cache downloaded models
            log_level: Logging level

        Raises:
            ImportError: If required dependencies are not installed
            ValueError: If invalid model configuration is provided
        """
        self.logger = setup_logger("asr_processor", log_level)

        # Convert string model name to enum if needed
        if isinstance(model_name, str):
            try:
                self.model_type = ASRModelType(model_name)
            except ValueError:
                if model_name.startswith("mlx-whisper"):
                    self.model_type = ASRModelType.CUSTOM
                elif model_name.startswith("coreml"):
                    self.model_type = ASRModelType.COREML_WHISPER
                else:
                    self.model_type = ASRModelType.CUSTOM
        else:
            self.model_type = model_name

        self.model_path = model_path
        self.use_mlx = use_mlx
        self.fallback_to_coreml = fallback_to_coreml
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".llama_voice" / "models"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Check dependencies
        if self.use_mlx and not HAS_MLX:
            self.logger.warning("MLX not available. Install with 'pip install mlx mlx-whisper'")
            if self.fallback_to_coreml and HAS_COREML:
                self.logger.info("Falling back to CoreML")
                self.use_mlx = False
            else:
                raise ImportError("MLX is required but not installed")

        if not self.use_mlx and not HAS_COREML:
            raise ImportError("Either MLX or CoreML is required")

        # Set transcription options
        self.options = TranscriptionOptions(language=language, beam_size=beam_size)

        # Initialize models
        self.mlx_model = None
        self.coreml_model = None
        self._load_models()

        self.logger.info(f"ASR Processor initialized with {self.model_type.value}")

    def _load_models(self) -> None:
        """
        Load the ASR models based on the configured backend.

        This method handles downloading models if needed and loading them
        with the appropriate backend (MLX or CoreML).

        Raises:
            ValueError: If model loading fails
            FileNotFoundError: If model file is not found
        """
        if self.use_mlx:
            self._load_mlx_model()
        else:
            self._load_coreml_model()

    def _load_mlx_model(self) -> None:
        """Load the MLX-optimized Whisper model."""
        if not HAS_MLX:
            raise ImportError("MLX is required to load MLX models")

        # Determine model path
        if self.model_type == ASRModelType.CUSTOM and self.model_path:
            model_path = Path(self.model_path)
        else:
            # Handle standard models
            model_name = self.model_type.value.replace("mlx-", "")
            model_dir = self.cache_dir / f"whisper-{model_name}-mlx"

            if not model_dir.exists():
                # Download model if not exists
                self.logger.info(f"Downloading {self.model_type.value} model...")
                self._download_model(self.model_type, model_dir)

            model_path = model_dir

        try:
            # Load the model using mlx_whisper
            self.logger.info(f"Loading MLX Whisper model from {model_path}")
            self.mlx_model = mlx_whisper.load_model(str(model_path))
            self.logger.info("MLX Whisper model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load MLX model: {str(e)}")
            if self.fallback_to_coreml and HAS_COREML:
                self.logger.info("Falling back to CoreML")
                self.use_mlx = False
                self._load_coreml_model()
            else:
                raise ValueError(f"Failed to load MLX model: {str(e)}")

    def _load_coreml_model(self) -> None:
        """Load the CoreML version of the Whisper model as fallback."""
        if not HAS_COREML:
            raise ImportError("CoreML is required to load CoreML models")

        # For CoreML, we need to check if there's a converted model or convert on the fly
        model_name = self.model_type.value.replace("mlx-", "").replace("coreml-", "")
        coreml_model_dir = self.cache_dir / f"whisper-{model_name}-coreml"

        if not coreml_model_dir.exists():
            self.logger.info(f"CoreML model not found at {coreml_model_dir}, converting...")
            coreml_model_dir.mkdir(parents=True, exist_ok=True)

            # TODO: Implement conversion from MLX to CoreML
            # For now, we'll assume models are pre-converted
            raise FileNotFoundError(f"CoreML model not found at {coreml_model_dir}")

        try:
            # Load CoreML model
            self.logger.info(f"Loading CoreML Whisper model from {coreml_model_dir}")
            self.coreml_model = load_coreml_model(str(coreml_model_dir))
            self.logger.info("CoreML Whisper model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load CoreML model: {str(e)}")
            raise ValueError(f"Failed to load CoreML model: {str(e)}")

    def _download_model(self, model_type: ASRModelType, target_dir: Path) -> None:
        """
        Download a model from the predefined URLs.

        Args:
            model_type: Type of model to download
            target_dir: Directory to save the downloaded model

        Raises:
            ValueError: If model download fails
        """
        import tarfile
        import tempfile
        import urllib.request

        if model_type not in self.MODEL_URLS:
            raise ValueError(f"No download URL for model type {model_type.value}")

        url = self.MODEL_URLS[model_type]
        target_dir.mkdir(parents=True, exist_ok=True)

        try:
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as temp_file:
                # Download the model
                self.logger.info(f"Downloading model from {url}")
                urllib.request.urlretrieve(url, temp_file.name)

                # Extract the model
                self.logger.info(f"Extracting model to {target_dir}")
                with tarfile.open(temp_file.name) as tar:
                    tar.extractall(path=target_dir)

                self.logger.info("Model downloaded and extracted successfully")
        except Exception as e:
            self.logger.error(f"Failed to download model: {str(e)}")
            raise ValueError(f"Failed to download model: {str(e)}")

    def transcribe(
        self,
        audio: Union[np.ndarray, AudioSegment, Dict[str, Any]],
        language: Optional[str] = None,
        word_timestamps: bool = False,
    ) -> Tuple[str, float]:
        """
        Transcribe audio using the loaded ASR model.

        Args:
            audio: Audio input as numpy array, AudioSegment, or feature dict
            language: Language to use for transcription (overrides default)
            word_timestamps: Whether to generate word-level timestamps

        Returns:
            Tuple of (transcription, confidence_score)

        Raises:
            ValueError: If audio format is invalid or transcription fails
        """
        # Preprocess audio if needed
        if isinstance(audio, AudioSegment):
            audio_array = audio.samples
            sample_rate = audio.sample_rate
        elif isinstance(audio, np.ndarray):
            audio_array = audio
            sample_rate = 16000  # Assume 16kHz if not specified
        elif isinstance(audio, dict) and "features" in audio:
            # Pre-extracted features
            return self._transcribe_from_features(audio)
        else:
            raise ValueError("Invalid audio format")

        # Set transcription options
        options = self.options
        if language:
            options.language = language
        options.word_timestamps = word_timestamps

        start_time = time.time()

        try:
            if self.use_mlx and self.mlx_model:
                # MLX Transcription
                # TODO: Implement actual MLX transcription call
                transcription = "Placeholder MLX Transcription"
                confidence = 0.95
            elif not self.use_mlx and self.coreml_model:
                # CoreML Transcription
                # TODO: Implement actual CoreML transcription call
                transcription = "Placeholder CoreML Transcription"
                confidence = 0.90
            else:
                self.logger.error("No ASR model loaded or available.")
                return "", 0.0
        except Exception as e:
            self.logger.error(f"Error during transcription: {str(e)}")
            return "", 0.0

        # TODO: Add actual transcription logic and return values

        return transcription, confidence  # Return placeholder results for now
