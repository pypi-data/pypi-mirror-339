"""
Voice Processor Pipeline implementation for fast, private voice interaction.

This module provides the core VoiceProcessor class that orchestrates the entire
pipeline from audio input to intent handling, prioritizing MLX-based processing
for optimal on-device performance.
"""

import logging
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import numpy as np
from llama_voice.processor.anonymizer import VoiceprintAnonymizer
from llama_voice.processor.asr import ASRProcessor
from llama_voice.processor.feature_extractor import AudioFeatureExtractor
from llama_voice.processor.intent_handler import IntentHandler
from llama_voice.processor.prosody_analyzer import ProsodyAnalyzer
from llama_voice.processor.secure_enclave import SecureEnclaveManager
from llama_voice.processor.text_repair import TextRepairProcessor
from llama_voice.processor.watermark_detector import WatermarkDetector
from llama_voice.utils.audio import AudioSegment
from llama_voice.utils.config import ProcessorConfig
from llama_voice.utils.logging import setup_logger


class ProcessingMode(Enum):
    """Processing mode for the voice processor pipeline."""

    STANDARD = "standard"  # Balance between speed and accuracy
    LOW_LATENCY = "low_latency"  # Prioritize speed
    HIGH_ACCURACY = "high_accuracy"  # Prioritize accuracy
    PRIVACY_FOCUSED = "privacy_focused"  # Max privacy protections


@dataclass
class ProcessingResult:
    """Results from voice processing pipeline."""

    # Original audio duration in seconds
    audio_duration: float

    # Processing timestamps
    processing_start_time: float
    processing_end_time: float

    # ASR results
    transcription: str
    transcription_confidence: float

    # Repaired text (if applicable)
    repaired_text: Optional[str] = None

    # Prosody analysis results
    prosody_features: Optional[Dict[str, Any]] = None

    # Intent analysis results
    detected_intent: Optional[str] = None
    intent_params: Optional[Dict[str, Any]] = None

    # Privacy indicators
    anonymization_applied: bool = False
    watermark_detected: bool = False

    # Performance metrics
    component_timings: Dict[str, float] = None

    @property
    def total_processing_time(self) -> float:
        """Calculate total processing time in seconds."""
        return self.processing_end_time - self.processing_start_time

    @property
    def realtime_factor(self) -> float:
        """Calculate realtime factor (processing_time / audio_duration)."""
        if self.audio_duration > 0:
            return self.total_processing_time / self.audio_duration
        return float("inf")


class VoiceProcessor:
    """
    End-to-end voice processing pipeline optimized for on-device performance.

    This class orchestrates the complete pipeline for voice processing:
    1. Audio anonymization (optional)
    2. Feature extraction
    3. ASR transcription
    4. Prosody analysis
    5. Text repair
    6. Watermark detection
    7. Intent handling

    The pipeline prioritizes MLX-based processing for all models with CoreML
    fallbacks when necessary.
    """

    def __init__(
        self,
        config: Optional[ProcessorConfig] = None,
        processing_mode: ProcessingMode = ProcessingMode.STANDARD,
        enable_anonymization: bool = True,
        enable_secure_enclave: bool = False,
        cache_dir: Optional[str] = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the voice processor pipeline.

        Args:
            config: Configuration object for the processor
            processing_mode: Processing mode to use
            enable_anonymization: Whether to enable voiceprint anonymization
            enable_secure_enclave: Whether to enable secure enclave for sensitive audio
            cache_dir: Directory to cache models and data
            log_level: Logging level
        """
        self.logger = setup_logger("voice_processor", log_level)
        self.logger.info(f"Initializing VoiceProcessor in {processing_mode.value} mode")

        self.config = config or ProcessorConfig()
        self.processing_mode = processing_mode
        self.enable_anonymization = enable_anonymization
        self.enable_secure_enclave = enable_secure_enclave
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".llama_voice"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self._init_components()

        self.logger.info("VoiceProcessor initialization complete")

    def _init_components(self) -> None:
        """Initialize all pipeline components."""
        # Initialize anonymizer if enabled
        self.anonymizer = (
            VoiceprintAnonymizer(
                mlx_model_path=self.config.anonymizer_model_path,
                enable_secure_storage=self.enable_secure_enclave,
            )
            if self.enable_anonymization
            else None
        )

        # Initialize feature extractor
        self.feature_extractor = AudioFeatureExtractor(
            model_path=self.config.feature_extractor_model_path,
            use_mlx=True,
            cache_dir=self.cache_dir,
        )

        # Initialize ASR processor with MLX whisper models
        self.asr = ASRProcessor(
            model_name=self.config.asr_model,
            use_mlx=True,
            fallback_to_coreml=True,
            language=self.config.language,
            beam_size=2 if self.processing_mode == ProcessingMode.LOW_LATENCY else 5,
            cache_dir=self.cache_dir,
        )

        # Initialize prosody analyzer
        self.prosody_analyzer = ProsodyAnalyzer(
            model_path=self.config.prosody_model_path,
            use_mlx=True,
            cache_dir=self.cache_dir,
        )

        # Initialize text repair processor
        self.repair_processor = TextRepairProcessor(
            model_path=self.config.repair_model_path,
            use_mlx=True,
            cache_dir=self.cache_dir,
        )

        # Initialize watermark detector
        self.watermark_detector = WatermarkDetector(
            model_path=self.config.watermark_model_path, cache_dir=self.cache_dir
        )

        # Initialize secure enclave manager if enabled
        self.secure_enclave = SecureEnclaveManager() if self.enable_secure_enclave else None

        # Initialize intent handler
        self.intent_handler = IntentHandler(
            config=self.config.intent_config, cache_dir=self.cache_dir
        )

    def process(
        self,
        audio: Union[str, Path, np.ndarray, AudioSegment],
        sample_rate: Optional[int] = None,
        apply_repair: bool = True,
        detect_intent: bool = True,
        return_prosody: bool = True,
        detect_watermark: bool = True,
        callback: Optional[Callable[[str, Any], None]] = None,
    ) -> ProcessingResult:
        """
        Process audio through the complete pipeline.

        Args:
            audio: Audio input (file path, numpy array, or AudioSegment)
            sample_rate: Sample rate if audio is numpy array
            apply_repair: Whether to apply text repair to ASR output
            detect_intent: Whether to detect intent from transcription
            return_prosody: Whether to analyze and return prosody features
            detect_watermark: Whether to detect audio watermarks
            callback: Optional callback function for progress updates
                     Function signature: callback(stage: str, data: Any)

        Returns:
            ProcessingResult object containing all processing results and metrics
        """
        start_time = time.time()
        component_timings = {}

        # Prepare result object
        result = ProcessingResult(
            audio_duration=0,  # Will be set after loading audio
            processing_start_time=start_time,
            processing_end_time=0,
            transcription="",
            transcription_confidence=0.0,
            component_timings=component_timings,
        )

        try:
            # Load and preprocess audio
            t0 = time.time()
            if isinstance(audio, (str, Path)):
                audio_segment = AudioSegment.from_file(audio)
            elif isinstance(audio, np.ndarray):
                if sample_rate is None:
                    raise ValueError("Sample rate must be provided for numpy array input")
                audio_segment = AudioSegment(audio, sample_rate)
            elif isinstance(audio, AudioSegment):
                audio_segment = audio
            else:
                raise TypeError(f"Unsupported audio type: {type(audio)}")

            result.audio_duration = audio_segment.duration
            component_timings["audio_loading"] = time.time() - t0

            if callback:
                callback("audio_loaded", {"duration": audio_segment.duration})

            # Apply anonymization if enabled
            if self.enable_anonymization and self.anonymizer:
                t0 = time.time()
                audio_segment = self.anonymizer.anonymize(audio_segment)
                component_timings["anonymization"] = time.time() - t0
                result.anonymization_applied = True

                if callback:
                    callback("anonymization_complete", {})

            # Extract audio features
            t0 = time.time()
            features = self.feature_extractor.extract(audio_segment)
            component_timings["feature_extraction"] = time.time() - t0

            if callback:
                callback("features_extracted", {})

            # Perform ASR
            t0 = time.time()
            transcription, confidence = self.asr.transcribe(features)
            component_timings["asr"] = time.time() - t0
            result.transcription = transcription
            result.transcription_confidence = confidence

            if callback:
                callback("asr_complete", {"text": transcription, "confidence": confidence})

            # Apply text repair if requested
            if apply_repair:
                t0 = time.time()
                repaired_text = self.repair_processor.repair(transcription)
                component_timings["text_repair"] = time.time() - t0
                result.repaired_text = repaired_text

                if callback:
                    callback("repair_complete", {"text": repaired_text})

            # Analyze prosody if requested
            if return_prosody:
                t0 = time.time()
                prosody = self.prosody_analyzer.analyze(audio_segment, transcription)
                component_timings["prosody_analysis"] = time.time() - t0
                result.prosody_features = prosody

                if callback:
                    callback("prosody_complete", {"features": prosody})

            # Detect watermark if requested
            if detect_watermark:
                t0 = time.time()
                watermark_detected = self.watermark_detector.detect(audio_segment)
                component_timings["watermark_detection"] = time.time() - t0
                result.watermark_detected = watermark_detected

                if callback:
                    callback("watermark_detection_complete", {"detected": watermark_detected})

            # Detect intent if requested
            if detect_intent:
                t0 = time.time()
                text_for_intent = (
                    result.repaired_text if result.repaired_text else result.transcription
                )
                intent, params = self.intent_handler.detect_intent(
                    text_for_intent, result.prosody_features
                )
                component_timings["intent_detection"] = time.time() - t0
                result.detected_intent = intent
                result.intent_params = params

                if callback:
                    callback(
                        "intent_detection_complete",
                        {"intent": intent, "params": params},
                    )

            # Store sensitive audio in secure enclave if enabled
            if self.enable_secure_enclave and self.secure_enclave:
                if result.watermark_detected or (
                    result.transcription_confidence < self.config.min_confidence_threshold
                ):
                    t0 = time.time()
                    self.secure_enclave.store_sensitive_audio(audio_segment, result.transcription)
                    component_timings["secure_storage"] = time.time() - t0

        except Exception as e:
            self.logger.error(f"Error in voice processing pipeline: {str(e)}", exc_info=True)
            raise

        finally:
            # Set end time and return result
            result.processing_end_time = time.time()

            if callback:
                callback(
                    "processing_complete",
                    {
                        "total_time": result.total_processing_time,
                        "realtime_factor": result.realtime_factor,
                    },
                )

            self.logger.info(
                f"Processing complete: {result.audio_duration:.2f}s audio processed in "
                f"{result.total_processing_time:.2f}s (RT factor: {result.realtime_factor:.2f}x)"
            )

            return result

    def shutdown(self) -> None:
        """Clean up resources and shutdown the processor."""
        self.logger.info("Shutting down VoiceProcessor")

        # Release model resources
        if hasattr(self, "asr") and self.asr:
            self.asr.unload_models()

        if hasattr(self, "secure_enclave") and self.secure_enclave:
            self.secure_enclave.close()
