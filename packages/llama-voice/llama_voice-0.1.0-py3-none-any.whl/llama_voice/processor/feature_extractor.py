"""
Audio Feature Extractor module for voice processing pipeline.

This module handles the extraction of audio features from raw audio signals,
optimized with MLX for performance on Apple Silicon devices.
"""

import logging
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np

# Conditional imports for different backends
try:
    import mlx.core as mx
    import mlx_audio

    HAS_MLX = True
except ImportError:
    HAS_MLX = False

try:
    import librosa

    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False

from llama_voice.utils.audio import AudioSegment
from llama_voice.utils.logging import setup_logger


class FeatureType(Enum):
    """Types of audio features supported by the extractor."""

    MEL_SPECTROGRAM = "mel_spectrogram"
    MFCC = "mfcc"
    FILTERBANK = "filterbank"
    WAV2VEC = "wav2vec"
    WHISPER_FEATURES = "whisper"
    CUSTOM = "custom"


@dataclass
class FeatureExtractionConfig:
    """Configuration for feature extraction."""

    feature_type: FeatureType = FeatureType.MEL_SPECTROGRAM
    sample_rate: int = 16000
    n_mels: int = 80
    n_fft: int = 400
    hop_length: int = 160
    fmin: float = 0.0
    fmax: Optional[float] = 8000.0
    n_mfcc: int = 13
    window_size_ms: float = 25.0
    stride_ms: float = 10.0
    normalize: bool = True
    pre_emphasis: Optional[float] = 0.97
    dither: float = 0.0


class AudioFeatureExtractor:
    """
    Audio Feature Extractor for voice processing.

    This class extracts various types of audio features (mel spectrograms, MFCCs, etc.)
    from raw audio signals, optimized for performance using MLX on Apple Silicon.
    """

    def __init__(
        self,
        feature_type: Union[str, FeatureType] = FeatureType.MEL_SPECTROGRAM,
        model_path: Optional[str] = None,
        config: Optional[FeatureExtractionConfig] = None,
        use_mlx: bool = True,
        cache_dir: Optional[Union[str, Path]] = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the audio feature extractor.

        Args:
            feature_type: Type of features to extract
            model_path: Path to a custom feature extraction model
            config: Configuration for feature extraction
            use_mlx: Whether to use MLX for computation
            cache_dir: Directory to cache models
            log_level: Logging level

        Raises:
            ImportError: If required dependencies are not installed
            ValueError: If invalid configuration is provided
        """
        self.logger = setup_logger("feature_extractor", log_level)

        # Convert string feature type to enum if needed
        if isinstance(feature_type, str):
            try:
                self.feature_type = FeatureType(feature_type)
            except ValueError:
                self.feature_type = FeatureType.CUSTOM
        else:
            self.feature_type = feature_type

        self.model_path = model_path
        self.config = config or FeatureExtractionConfig(feature_type=self.feature_type)
        self.use_mlx = use_mlx and HAS_MLX
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".llama_voice" / "models"

        # Check dependencies
        if self.use_mlx and not HAS_MLX:
            self.logger.warning("MLX not available. Install with 'pip install mlx mlx-audio'")
            self.use_mlx = False

        if not HAS_LIBROSA and not self.use_mlx:
            self.logger.warning(
                "Neither MLX nor librosa available. Audio feature extraction may be limited."
            )

        # Load models or initialize feature extractors
        self._init_extractors()

        self.logger.info(f"Audio Feature Extractor initialized with {self.feature_type.value}")

    def _init_extractors(self) -> None:
        """
        Initialize feature extractors based on the selected type.

        This method sets up the appropriate feature extraction pipeline based on
        the selected feature type and backend (MLX or CPU).
        """
        if self.feature_type == FeatureType.WAV2VEC:
            self._init_wav2vec()
        elif self.feature_type == FeatureType.CUSTOM and self.model_path:
            self._init_custom_model()
        else:
            # For standard features (mel, mfcc, filterbank), no model loading needed
            pass

        # If using MLX, precompile the feature extraction functions
        if self.use_mlx:
            self._precompile_mlx_functions()

    def _init_wav2vec(self) -> None:
        """Initialize Wav2Vec feature extractor."""
        if self.use_mlx:
            # Check if MLX-Audio has Wav2Vec support
            if not hasattr(mlx_audio, "wav2vec"):
                self.logger.warning("MLX-Audio does not have Wav2Vec support")
                return

            model_path = self.model_path
            if not model_path:
                # Use default model path
                model_path = self.cache_dir / "wav2vec-mlx"

                # Download if not exists
                if not model_path.exists():
                    self.logger.info(f"Downloading Wav2Vec model to {model_path}")
                    self._download_wav2vec_model(model_path)

            try:
                # Load Wav2Vec model with MLX
                self.logger.info(f"Loading Wav2Vec model from {model_path}")
                self.wav2vec_model = mlx_audio.wav2vec.load_model(str(model_path))
                self.logger.info("Wav2Vec model loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to load Wav2Vec model: {str(e)}")
                self.wav2vec_model = None

    def _init_custom_model(self) -> None:
        """Initialize a custom feature extraction model."""
        if not self.model_path:
            self.logger.warning("Custom feature type selected but no model path provided")
            return

        model_path = Path(self.model_path)
        if not model_path.exists():
            self.logger.error(f"Custom model not found at {model_path}")
            return

        try:
            # Load custom model (implementation depends on model format)
            self.logger.info(f"Loading custom feature extraction model from {model_path}")
            # self.custom_model = ...
            self.logger.info("Custom model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load custom model: {str(e)}")

    def _precompile_mlx_functions(self) -> None:
        """Precompile MLX functions for faster execution."""
        if not self.use_mlx:
            return

        # Precompile common feature extraction functions
        if self.feature_type == FeatureType.MEL_SPECTROGRAM:
            # Create a small sample for compilation
            dummy_audio = mx.random.uniform(shape=(16000,))

            # Precompile mel spectrogram extraction
            mlx_audio.transforms.melspectrogram(
                dummy_audio,
                sample_rate=self.config.sample_rate,
                n_fft=self.config.n_fft,
                n_mels=self.config.n_mels,
                hop_length=self.config.hop_length,
                fmin=self.config.fmin,
                fmax=self.config.fmax,
            )

        elif self.feature_type == FeatureType.MFCC:
            # Precompile MFCC extraction
            dummy_audio = mx.random.uniform(shape=(16000,))

            mlx_audio.transforms.mfcc(
                dummy_audio,
                sample_rate=self.config.sample_rate,
                n_mfcc=self.config.n_mfcc,
                n_fft=self.config.n_fft,
                hop_length=self.config.hop_length,
                n_mels=self.config.n_mels,
                fmin=self.config.fmin,
                fmax=self.config.fmax,
            )

    def _download_wav2vec_model(self, target_dir: Path) -> None:
        """
        Download a Wav2Vec model for MLX.

        Args:
            target_dir: Directory to save the downloaded model

        Raises:
            ValueError: If model download fails
        """
        import tarfile
        import tempfile
        import urllib.request

        # URL for MLX-compatible Wav2Vec model
        url = "https://huggingface.co/mlx-community/wav2vec-mlx/resolve/main/wav2vec-mlx.tar.gz"
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

    def extract(
        self,
        audio: Union[np.ndarray, AudioSegment],
        feature_type: Optional[FeatureType] = None,
        config_override: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Extract features from audio input.

        Args:
            audio: Audio input as numpy array or AudioSegment
            feature_type: Override the default feature type
            config_override: Override specific config parameters

        Returns:
            Dictionary containing the extracted features and metadata

        Raises:
            ValueError: If audio format is invalid or feature extraction fails
        """
        # Preprocess audio if needed
        if isinstance(audio, AudioSegment):
            audio_array = audio.samples
            sample_rate = audio.sample_rate
        elif isinstance(audio, np.ndarray):
            audio_array = audio
            sample_rate = self.config.sample_rate
        else:
            raise ValueError("Invalid audio format")

        # Apply configuration overrides
        current_config = self.config
        if config_override:
            # Create a copy of the config and update with overrides
            config_dict = {
                k: getattr(current_config, k) for k in current_config.__dataclass_fields__
            }
            config_dict.update(config_override)
            current_config = FeatureExtractionConfig(**config_dict)

        # Get feature type to extract
        extract_type = feature_type or self.feature_type

        start_time = time.time()

        try:
            # Extract features based on type
            if extract_type == FeatureType.MEL_SPECTROGRAM:
                features = self._extract_mel_spectrogram(audio_array, sample_rate, current_config)
            elif extract_type == FeatureType.MFCC:
                features = self._extract_mfcc(audio_array, sample_rate, current_config)
            elif extract_type == FeatureType.FILTERBANK:
                features = self._extract_filterbank(audio_array, sample_rate, current_config)
            elif extract_type == FeatureType.WAV2VEC:
                features = self._extract_wav2vec(audio_array, sample_rate)
            elif extract_type == FeatureType.WHISPER_FEATURES:
                features = self._extract_whisper_features(audio_array, sample_rate)
            elif extract_type == FeatureType.CUSTOM:
                features = self._extract_custom(audio_array, sample_rate)
            else:
                raise ValueError(f"Unsupported feature type: {extract_type}")

            elapsed = time.time() - start_time
            self.logger.info(
                f"Feature extraction ({extract_type.value}) completed in {elapsed:.4f}s"
            )

            # Convert features to numpy if they're MLX arrays
            if self.use_mlx and isinstance(features, mx.array):
                features = features.tolist()

            # Return features with metadata
            return {
                "features": features,
                "type": extract_type.value,
                "config": {
                    k: getattr(current_config, k) for k in current_config.__dataclass_fields__
                },
                "sample_rate": sample_rate,
                "duration": len(audio_array) / sample_rate,
                "extraction_time": elapsed,
            }

        except Exception as e:
            self.logger.error(f"Feature extraction failed: {str(e)}", exc_info=True)
            raise ValueError(f"Feature extraction failed: {str(e)}")

    def _extract_mel_spectrogram(
        self, audio: np.ndarray, sample_rate: int, config: FeatureExtractionConfig
    ) -> np.ndarray:
        """
        Extract mel spectrogram features.

        Args:
            audio: Audio samples
            sample_rate: Sample rate of the audio
            config: Feature extraction configuration

        Returns:
            Mel spectrogram features
        """
        if self.use_mlx:
            # Convert to MLX array if it's numpy
            if isinstance(audio, np.ndarray):
                audio = mx.array(audio)

            # Apply pre-emphasis if configured
            if config.pre_emphasis:
                audio = mlx_audio.transforms.preemphasis(audio, coefficient=config.pre_emphasis)

            # Add dither if configured
            if config.dither > 0:
                noise = mx.random.uniform(low=-config.dither, high=config.dither, shape=audio.shape)
                audio = audio + noise

            # Extract mel spectrogram using MLX-Audio
            mel_spec = mlx_audio.transforms.melspectrogram(
                audio,
                sample_rate=config.sample_rate,
                n_fft=config.n_fft,
                hop_length=config.hop_length,
                n_mels=config.n_mels,
                fmin=config.fmin,
                fmax=config.fmax if config.fmax else sample_rate / 2,
            )

            # Log mel spectrogram
            mel_spec = mx.log(mx.maximum(mel_spec, 1e-10))

            # Normalize if configured
            if config.normalize:
                mel_spec = (mel_spec - mx.mean(mel_spec)) / (mx.std(mel_spec) + 1e-8)

            return mel_spec
        else:
            # Fallback to librosa if available
            if HAS_LIBROSA:
                # Apply pre-emphasis if configured
                if config.pre_emphasis:
                    audio = librosa.effects.preemphasis(audio, coef=config.pre_emphasis)

                # Add dither if configured
                if config.dither > 0:
                    noise = np.random.uniform(
                        low=-config.dither, high=config.dither, size=audio.shape
                    )
                    audio = audio + noise

                # Extract mel spectrogram using librosa
                mel_spec = librosa.feature.melspectrogram(
                    y=audio,
                    sr=sample_rate,
                    n_fft=config.n_fft,
                    hop_length=config.hop_length,
                    n_mels=config.n_mels,
                    fmin=config.fmin,
                    fmax=config.fmax if config.fmax else sample_rate / 2,
                )

                # Log mel spectrogram
                mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

                # Normalize if configured
                if config.normalize:
                    mel_spec = (mel_spec - np.mean(mel_spec)) / (np.std(mel_spec) + 1e-8)

                return mel_spec
            else:
                raise ImportError(
                    "Neither MLX nor librosa is available for mel spectrogram extraction"
                )

    def _extract_mfcc(
        self, audio: np.ndarray, sample_rate: int, config: FeatureExtractionConfig
    ) -> np.ndarray:
        """
        Extract MFCC features.

        Args:
            audio: Audio samples
            sample_rate: Sample rate of the audio
            config: Feature extraction configuration

        Returns:
            MFCC features
        """
        if self.use_mlx:
            # Convert to MLX array if it's numpy
            if isinstance(audio, np.ndarray):
                audio = mx.array(audio)

            # Apply pre-emphasis if configured
            if config.pre_emphasis:
                audio = mlx_audio.transforms.preemphasis(audio, coefficient=config.pre_emphasis)

            # Extract MFCCs using MLX-Audio
            mfccs = mlx_audio.transforms.mfcc(
                audio,
                sample_rate=config.sample_rate,
                n_mfcc=config.n_mfcc,
                n_fft=config.n_fft,
                hop_length=config.hop_length,
                n_mels=config.n_mels,
                fmin=config.fmin,
                fmax=config.fmax if config.fmax else sample_rate / 2,
            )

            # Normalize if configured
            if config.normalize:
                mfccs = (mfccs - mx.mean(mfccs)) / (mx.std(mfccs) + 1e-8)

            return mfccs
        else:
            # Fallback to librosa if available
            if HAS_LIBROSA:
                # Apply pre-emphasis if configured
                if config.pre_emphasis:
                    audio = librosa.effects.preemphasis(audio, coef=config.pre_emphasis)

                # Extract MFCCs using librosa
                mfccs = librosa.feature.mfcc(
                    y=audio,
                    sr=sample_rate,
                    n_mfcc=config.n_mfcc,
                    n_fft=config.n_fft,
                    hop_length=config.hop_length,
                    n_mels=config.n_mels,
                    fmin=config.fmin,
                    fmax=config.fmax if config.fmax else sample_rate / 2,
                )

                # Normalize if configured
                if config.normalize:
                    mfccs = (mfccs - np.mean(mfccs)) / (np.std(mfccs) + 1e-8)

                return mfccs
            else:
                raise ImportError("Neither MLX nor librosa is available for MFCC extraction")

    def _extract_filterbank(
        self, audio: np.ndarray, sample_rate: int, config: FeatureExtractionConfig
    ) -> np.ndarray:
        """
        Extract filterbank features.

        Args:
            audio: Audio samples
            sample_rate: Sample rate of the audio
            config: Feature extraction configuration

        Returns:
            Filterbank features
        """
        # Filterbank is essentially mel spectrogram without the log transform
        if self.use_mlx:
            # Convert to MLX array if it's numpy
            if isinstance(audio, np.ndarray):
                audio = mx.array(audio)

            # Apply pre-emphasis if configured
            if config.pre_emphasis:
                audio = mlx_audio.transforms.preemphasis(audio, coefficient=config.pre_emphasis)

            # Extract filterbank using MLX-Audio (mel spectrogram without log)
            fbank = mlx_audio.transforms.melspectrogram(
                audio,
                sample_rate=config.sample_rate,
                n_fft=config.n_fft,
                hop_length=config.hop_length,
                n_mels=config.n_mels,
                fmin=config.fmin,
                fmax=config.fmax if config.fmax else sample_rate / 2,
            )

            # Normalize if configured
            if config.normalize:
                fbank = (fbank - mx.mean(fbank)) / (mx.std(fbank) + 1e-8)

            return fbank
        else:
            # Fallback to librosa if available
            if HAS_LIBROSA:
                # Apply pre-emphasis if configured
                if config.pre_emphasis:
                    audio = librosa.effects.preemphasis(audio, coef=config.pre_emphasis)

                # Extract filterbank using librosa
                fbank = librosa.feature.melspectrogram(
                    y=audio,
                    sr=sample_rate,
                    n_fft=config.n_fft,
                    hop_length=config.hop_length,
                    n_mels=config.n_mels,
                    fmin=config.fmin,
                    fmax=config.fmax if config.fmax else sample_rate / 2,
                )

                # Normalize if configured
                if config.normalize:
                    fbank = (fbank - np.mean(fbank)) / (np.std(fbank) + 1e-8)

                return fbank
            else:
                raise ImportError("Neither MLX nor librosa is available for filterbank extraction")

    def _extract_wav2vec(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Extract Wav2Vec features.

        Args:
            audio: Audio samples
            sample_rate: Sample rate of the audio

        Returns:
            Wav2Vec features
        """
        if not hasattr(self, "wav2vec_model") or self.wav2vec_model is None:
            raise ValueError("Wav2Vec model not loaded")

        # Ensure correct sample rate
        target_sr = 16000  # Wav2Vec expects 16kHz
        if sample_rate != target_sr:
            if HAS_LIBROSA:
                audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=target_sr)
            else:
                raise ImportError("Librosa is required for resampling")

        # Convert to MLX array if using MLX
        if self.use_mlx and isinstance(audio, np.ndarray):
            audio = mx.array(audio)

        # Extract features
        features = self.wav2vec_model.extract_features(audio)

        return features

    def _extract_whisper_features(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Extract features compatible with Whisper models.

        Args:
            audio: Audio samples
            sample_rate: Sample rate of the audio

        Returns:
            Whisper-compatible features
        """
        try:
            from mlx_whisper import load_audio

            # Ensure correct sample rate
            target_sr = 16000  # Whisper expects 16kHz
            if sample_rate != target_sr:
                if HAS_LIBROSA:
                    audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=target_sr)
                else:
                    raise ImportError("Librosa is required for resampling")

            # Load audio with Whisper processor
            whisper_audio = load_audio(audio, target_sr)

            # Return the processed audio
            return whisper_audio
        except ImportError:
            self.logger.error("mlx_whisper is required for Whisper feature extraction")
            raise ImportError("mlx_whisper is required for Whisper feature extraction")

    def _extract_custom(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Extract features using a custom model.

        Args:
            audio: Audio samples
            sample_rate: Sample rate of the audio

        Returns:
            Custom features
        """
        # Implementation depends on the custom model
        raise NotImplementedError("Custom feature extraction not implemented")
