"""
Tests for the VoiceProcessor pipeline.

This module contains tests for the complete voice processing pipeline and its components.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from llama_voice.processor.pipeline import ProcessingMode, VoiceProcessor
from llama_voice.utils.audio import AudioSegment


class TestVoiceProcessor:
    """Test suite for the VoiceProcessor class."""

    @pytest.fixture
    def sample_audio(self):
        """Create a sample audio for testing."""
        # Generate 1 second of sample audio (sine wave at 440Hz)
        sample_rate = 16000
        duration = 1.0  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration))
        samples = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        return AudioSegment(samples, sample_rate)

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary directory for cache."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield tmp_dir

    def test_init(self, temp_cache_dir):
        """Test VoiceProcessor initialization."""
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=False,
            enable_secure_enclave=False,
            cache_dir=temp_cache_dir,
        )

        assert processor.processing_mode == ProcessingMode.STANDARD
        assert processor.enable_anonymization is False
        assert processor.enable_secure_enclave is False
        assert processor.cache_dir == Path(temp_cache_dir)

        # Check component initialization
        assert processor.feature_extractor is not None
        assert processor.asr is not None
        assert processor.prosody_analyzer is not None
        assert processor.repair_processor is not None
        assert processor.watermark_detector is not None
        assert processor.intent_handler is not None
        assert processor.anonymizer is None  # Should be None since anonymization is disabled
        assert processor.secure_enclave is None  # Should be None since secure enclave is disabled

    def test_init_with_anonymization(self, temp_cache_dir):
        """Test VoiceProcessor initialization with anonymization."""
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=True,
            enable_secure_enclave=False,
            cache_dir=temp_cache_dir,
        )

        assert processor.enable_anonymization is True
        assert processor.anonymizer is not None

    @patch("llama_voice.processor.feature_extractor.AudioFeatureExtractor.extract")
    @patch("llama_voice.processor.asr.ASRProcessor.transcribe")
    @patch("llama_voice.processor.text_repair.TextRepairProcessor.repair")
    def test_process_basic(
        self, mock_repair, mock_transcribe, mock_extract, sample_audio, temp_cache_dir
    ):
        """Test basic processing flow without anonymization or secure enclave."""
        # Set up mocks
        mock_extract.return_value = {"features": np.zeros((80, 100))}
        mock_transcribe.return_value = ("This is a test.", 0.95)
        mock_repair.return_value = "This is a test."

        # Initialize processor with mocked components
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=False,
            enable_secure_enclave=False,
            cache_dir=temp_cache_dir,
        )

        # Process audio
        result = processor.process(
            audio=sample_audio,
            apply_repair=True,
            detect_intent=False,
            return_prosody=False,
            detect_watermark=False,
        )

        # Verify results
        assert result.transcription == "This is a test."
        assert result.transcription_confidence == 0.95
        assert result.repaired_text == "This is a test."
        assert result.audio_duration == 1.0

        # Verify mocks were called
        mock_extract.assert_called_once()
        mock_transcribe.assert_called_once()
        mock_repair.assert_called_once_with("This is a test.")

    @patch("llama_voice.processor.anonymizer.VoiceprintAnonymizer.anonymize")
    @patch("llama_voice.processor.feature_extractor.AudioFeatureExtractor.extract")
    @patch("llama_voice.processor.asr.ASRProcessor.transcribe")
    def test_process_with_anonymization(
        self,
        mock_transcribe,
        mock_extract,
        mock_anonymize,
        sample_audio,
        temp_cache_dir,
    ):
        """Test processing with anonymization."""
        # Set up mocks
        mock_anonymize.return_value = sample_audio
        mock_extract.return_value = {"features": np.zeros((80, 100))}
        mock_transcribe.return_value = ("This is a test.", 0.95)

        # Initialize processor with anonymization
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=True,
            enable_secure_enclave=False,
            cache_dir=temp_cache_dir,
        )

        # Process audio
        result = processor.process(
            audio=sample_audio,
            apply_repair=False,
            detect_intent=False,
            return_prosody=False,
            detect_watermark=False,
        )

        # Verify results
        assert result.transcription == "This is a test."
        assert result.anonymization_applied is True

        # Verify anonymization was called
        mock_anonymize.assert_called_once()

    @patch("llama_voice.processor.feature_extractor.AudioFeatureExtractor.extract")
    @patch("llama_voice.processor.asr.ASRProcessor.transcribe")
    @patch("llama_voice.processor.prosody_analyzer.ProsodyAnalyzer.analyze")
    @patch("llama_voice.processor.intent_handler.IntentHandler.detect_intent")
    def test_process_with_prosody_and_intent(
        self,
        mock_detect_intent,
        mock_analyze_prosody,
        mock_transcribe,
        mock_extract,
        sample_audio,
        temp_cache_dir,
    ):
        """Test processing with prosody analysis and intent detection."""
        # Set up mocks
        mock_extract.return_value = {"features": np.zeros((80, 100))}
        mock_transcribe.return_value = ("Play some music.", 0.98)

        prosody_result = {
            "pitch": {"mean": 120.0},
            "energy": {"mean": 0.8},
            "speech_rate": {"speech_rate": 4.5},
            "emotion": {"dominant_emotion": "neutral"},
        }
        mock_analyze_prosody.return_value = prosody_result

        mock_detect_intent.return_value = ("play_media", {"media_type": "music"})

        # Initialize processor
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=False,
            enable_secure_enclave=False,
            cache_dir=temp_cache_dir,
        )

        # Process audio
        result = processor.process(
            audio=sample_audio,
            apply_repair=False,
            detect_intent=True,
            return_prosody=True,
            detect_watermark=False,
        )

        # Verify results
        assert result.transcription == "Play some music."
        assert result.prosody_features == prosody_result
        assert result.detected_intent == "play_media"
        assert result.intent_params == {"media_type": "music"}

        # Verify mocks were called
        mock_analyze_prosody.assert_called_once()
        mock_detect_intent.assert_called_once_with("Play some music.", prosody_result)

    @patch("llama_voice.processor.feature_extractor.AudioFeatureExtractor.extract")
    @patch("llama_voice.processor.asr.ASRProcessor.transcribe")
    @patch("llama_voice.processor.watermark_detector.WatermarkDetector.detect")
    @patch("llama_voice.processor.secure_enclave.SecureEnclaveManager.store_sensitive_audio")
    def test_process_with_watermark_and_secure_enclave(
        self,
        mock_store,
        mock_detect_watermark,
        mock_transcribe,
        mock_extract,
        sample_audio,
        temp_cache_dir,
    ):
        """Test processing with watermark detection and secure enclave."""
        # Set up mocks
        mock_extract.return_value = {"features": np.zeros((80, 100))}
        mock_transcribe.return_value = ("This is a synthetic voice.", 0.92)
        mock_detect_watermark.return_value = True
        mock_store.return_value = "test-entry-id"

        # Initialize processor with secure enclave
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=False,
            enable_secure_enclave=True,
            cache_dir=temp_cache_dir,
        )

        # Process audio
        result = processor.process(
            audio=sample_audio,
            apply_repair=False,
            detect_intent=False,
            return_prosody=False,
            detect_watermark=True,
        )

        # Verify results
        assert result.transcription == "This is a synthetic voice."
        assert result.watermark_detected is True

        # Verify mocks were called
        mock_detect_watermark.assert_called_once()
        mock_store.assert_called_once()

    def test_shutdown(self, temp_cache_dir):
        """Test processor shutdown."""
        # Initialize with mock components
        processor = VoiceProcessor(
            processing_mode=ProcessingMode.STANDARD,
            enable_anonymization=False,
            enable_secure_enclave=False,
            cache_dir=temp_cache_dir,
        )

        # Mock the components
        processor.asr = MagicMock()
        processor.asr.unload_models = MagicMock()

        # Call shutdown
        processor.shutdown()

        # Verify components were cleaned up
        processor.asr.unload_models.assert_called_once()
