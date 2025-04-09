"""
Audio utility module for handling audio data in the voice processing pipeline.

This module provides the AudioSegment class and related utilities for working
with audio data across the voice processing pipeline.
"""

import wave
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np

# Conditional imports
try:
    import librosa

    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False


class AudioFormat(Enum):
    """Supported audio formats."""

    WAV = "wav"
    PCM = "pcm"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"
    CAF = "caf"  # Core Audio Format (common on Apple devices)


@dataclass
class AudioMetadata:
    """Metadata for audio files."""

    format: AudioFormat
    sample_rate: int
    channels: int
    duration: float
    bit_depth: int
    encoding: str = "pcm"
    custom_metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.custom_metadata is None:
            self.custom_metadata = {}


class AudioSegment:
    """
    AudioSegment class for handling audio data.

    This class provides a consistent interface for working with audio data
    throughout the voice processing pipeline, with methods for loading, saving,
    and manipulating audio.
    """

    def __init__(
        self,
        samples: np.ndarray,
        sample_rate: int,
        channels: int = 1,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an AudioSegment.

        Args:
            samples: Audio samples as numpy array
            sample_rate: Sample rate in Hz
            channels: Number of audio channels
            metadata: Optional metadata

        Raises:
            ValueError: If samples or sample_rate are invalid
        """
        # Validate and store samples
        if not isinstance(samples, np.ndarray):
            raise ValueError("Samples must be a numpy array")

        # Convert to float32 if not already
        if samples.dtype != np.float32:
            # Normalize based on dtype to range [-1.0, 1.0]
            if samples.dtype == np.int16:
                samples = samples.astype(np.float32) / 32768.0
            elif samples.dtype == np.int32:
                samples = samples.astype(np.float32) / 2147483648.0
            elif samples.dtype == np.uint8:
                samples = (samples.astype(np.float32) - 128) / 128.0
            else:
                samples = samples.astype(np.float32)

            # Ensure range is [-1.0, 1.0]
            if np.max(np.abs(samples)) > 1.0:
                samples = samples / np.max(np.abs(samples))

        # Store samples
        self.samples = samples
        self.sample_rate = sample_rate
        self.channels = channels

        # Initialize metadata
        self.metadata = metadata or {}

        # Calculate duration
        self.duration = len(samples) / sample_rate

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "AudioSegment":
        """
        Create an AudioSegment from an audio file.

        Args:
            file_path: Path to the audio file

        Returns:
            AudioSegment instance

        Raises:
            ValueError: If file cannot be loaded
            FileNotFoundError: If file does not exist
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Determine file format
        file_format = file_path.suffix.lower()[1:]

        try:
            # Use librosa if available for broad format support
            if HAS_LIBROSA:
                samples, sample_rate = librosa.load(str(file_path), sr=None, mono=True)
                return cls(samples, sample_rate)

            # Fall back to wave module for WAV files
            elif file_format == "wav":
                with wave.open(str(file_path), "rb") as wav_file:
                    sample_rate = wav_file.getframerate()
                    channels = wav_file.getnchannels()
                    n_frames = wav_file.getnframes()
                    sample_width = wav_file.getsampwidth()

                    # Read audio data
                    frame_data = wav_file.readframes(n_frames)

                    # Convert to numpy array based on sample width
                    if sample_width == 1:  # 8-bit PCM
                        samples = np.frombuffer(frame_data, dtype=np.uint8)
                        samples = (samples.astype(np.float32) - 128) / 128.0
                    elif sample_width == 2:  # 16-bit PCM
                        samples = np.frombuffer(frame_data, dtype=np.int16)
                        samples = samples.astype(np.float32) / 32768.0
                    elif sample_width == 4:  # 32-bit PCM
                        samples = np.frombuffer(frame_data, dtype=np.int32)
                        samples = samples.astype(np.float32) / 2147483648.0
                    else:
                        raise ValueError(f"Unsupported sample width: {sample_width}")

                    # Handle multi-channel audio (convert to mono by averaging)
                    if channels > 1:
                        samples = samples.reshape(-1, channels)
                        samples = np.mean(samples, axis=1)

                    return cls(samples, sample_rate, 1)
            else:
                raise ValueError(f"Unsupported audio format: {file_format} (librosa not available)")

        except Exception as e:
            raise ValueError(f"Failed to load audio file: {str(e)}")

    @classmethod
    def from_bytes(
        cls, data: bytes, sample_rate: int, sample_width: int = 2, channels: int = 1
    ) -> "AudioSegment":
        """
        Create an AudioSegment from raw audio bytes.

        Args:
            data: Raw audio bytes
            sample_rate: Sample rate in Hz
            sample_width: Width of each sample in bytes
            channels: Number of audio channels

        Returns:
            AudioSegment instance

        Raises:
            ValueError: If data cannot be converted
        """
        try:
            # Convert bytes to numpy array based on sample width
            if sample_width == 1:  # 8-bit PCM
                samples = np.frombuffer(data, dtype=np.uint8)
                samples = (samples.astype(np.float32) - 128) / 128.0
            elif sample_width == 2:  # 16-bit PCM
                samples = np.frombuffer(data, dtype=np.int16)
                samples = samples.astype(np.float32) / 32768.0
            elif sample_width == 4:  # 32-bit PCM
                samples = np.frombuffer(data, dtype=np.int32)
                samples = samples.astype(np.float32) / 2147483648.0
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")

            # Handle multi-channel audio (convert to mono by averaging)
            if channels > 1:
                samples = samples.reshape(-1, channels)
                samples = np.mean(samples, axis=1)

            return cls(samples, sample_rate, 1)

        except Exception as e:
            raise ValueError(f"Failed to create AudioSegment from bytes: {str(e)}")

    def to_file(
        self,
        file_path: Union[str, Path],
        format: Optional[Union[str, AudioFormat]] = None,
        sample_width: int = 2,
    ) -> None:
        """
        Save the AudioSegment to a file.

        Args:
            file_path: Path to save the audio file
            format: Audio format to use (inferred from file extension if None)
            sample_width: Width of each sample in bytes

        Raises:
            ValueError: If file cannot be saved
        """
        file_path = Path(file_path)

        # Determine format if not specified
        if format is None:
            format = file_path.suffix.lower()[1:]

        # Convert string format to enum if needed
        if isinstance(format, str):
            try:
                format = AudioFormat(format)
            except ValueError:
                raise ValueError(f"Unsupported audio format: {format}")

        try:
            # Use librosa/soundfile if available for broad format support
            if HAS_LIBROSA:
                import soundfile as sf

                sf.write(str(file_path), self.samples, self.sample_rate)

            # Fall back to wave module for WAV files
            elif format == AudioFormat.WAV:
                self._save_as_wav(file_path, sample_width)

            else:
                raise ValueError(
                    f"Unsupported audio format: {format.value} (librosa not available)"
                )

        except Exception as e:
            raise ValueError(f"Failed to save audio file: {str(e)}")

    def _save_as_wav(self, file_path: Path, sample_width: int) -> None:
        """
        Save the AudioSegment as a WAV file.

        Args:
            file_path: Path to save the WAV file
            sample_width: Width of each sample in bytes

        Raises:
            ValueError: If file cannot be saved
        """
        # Convert float32 samples to specified sample width
        if sample_width == 1:  # 8-bit PCM
            samples = (self.samples * 128 + 128).clip(0, 255).astype(np.uint8)
        elif sample_width == 2:  # 16-bit PCM
            samples = (self.samples * 32767).clip(-32768, 32767).astype(np.int16)
        elif sample_width == 4:  # 32-bit PCM
            samples = (self.samples * 2147483647).clip(-2147483648, 2147483647).astype(np.int32)
        else:
            raise ValueError(f"Unsupported sample width: {sample_width}")

        # Write WAV file
        with wave.open(str(file_path), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(samples.tobytes())

    def to_bytes(self, sample_width: int = 2) -> bytes:
        """
        Convert the AudioSegment to raw audio bytes.

        Args:
            sample_width: Width of each sample in bytes

        Returns:
            Raw audio bytes

        Raises:
            ValueError: If conversion fails
        """
        try:
            # Convert float32 samples to specified sample width
            if sample_width == 1:  # 8-bit PCM
                samples = (self.samples * 128 + 128).clip(0, 255).astype(np.uint8)
            elif sample_width == 2:  # 16-bit PCM
                samples = (self.samples * 32767).clip(-32768, 32767).astype(np.int16)
            elif sample_width == 4:  # 32-bit PCM
                samples = (self.samples * 2147483647).clip(-2147483648, 2147483647).astype(np.int32)
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")

            return samples.tobytes()

        except Exception as e:
            raise ValueError(f"Failed to convert AudioSegment to bytes: {str(e)}")

    def resample(self, target_sample_rate: int) -> "AudioSegment":
        """
        Resample the audio to a new sample rate.

        Args:
            target_sample_rate: Target sample rate in Hz

        Returns:
            Resampled AudioSegment

        Raises:
            ValueError: If resampling fails
        """
        if target_sample_rate == self.sample_rate:
            return self

        try:
            # Use librosa if available
            if HAS_LIBROSA:
                resampled = librosa.resample(
                    self.samples, orig_sr=self.sample_rate, target_sr=target_sample_rate
                )
                return AudioSegment(resampled, target_sample_rate, self.channels, self.metadata)

            # Simple resampling implementation (for demonstration)
            # Note: This is a very basic implementation and is not high quality
            else:
                ratio = target_sample_rate / self.sample_rate
                output_length = int(len(self.samples) * ratio)
                indices = np.linspace(0, len(self.samples) - 1, output_length)
                resampled = np.interp(indices, np.arange(len(self.samples)), self.samples)
                return AudioSegment(resampled, target_sample_rate, self.channels, self.metadata)

        except Exception as e:
            raise ValueError(f"Failed to resample audio: {str(e)}")

    def trim_silence(self, threshold: float = 0.01, padding_ms: int = 100) -> "AudioSegment":
        """
        Trim silence from the beginning and end of the audio.

        Args:
            threshold: Amplitude threshold below which is considered silence
            padding_ms: Padding in milliseconds to add after trimming

        Returns:
            Trimmed AudioSegment
        """
        # Find non-silent parts
        amplitude = np.abs(self.samples)
        non_silent = amplitude > threshold

        if not np.any(non_silent):
            # If everything is below threshold, return a short segment of silence
            return AudioSegment(
                np.zeros(int(self.sample_rate * 0.1)),
                self.sample_rate,
                self.channels,
                self.metadata,
            )

        # Find start and end indices
        start_idx = np.where(non_silent)[0][0]
        end_idx = np.where(non_silent)[0][-1]

        # Add padding
        padding_samples = int(self.sample_rate * padding_ms / 1000)
        start_idx = max(0, start_idx - padding_samples)
        end_idx = min(len(self.samples) - 1, end_idx + padding_samples)

        # Trim audio
        trimmed_samples = self.samples[start_idx : end_idx + 1]

        return AudioSegment(trimmed_samples, self.sample_rate, self.channels, self.metadata)

    def normalize(self, target_db: float = -3.0) -> "AudioSegment":
        """
        Normalize audio volume to target dB.

        Args:
            target_db: Target peak dB level

        Returns:
            Normalized AudioSegment
        """
        # Calculate current peak
        peak = np.max(np.abs(self.samples))

        # If effectively silent, return unchanged
        if peak < 1e-8:
            return self

        # Calculate target peak (0 dB = 1.0 amplitude)
        target_peak = 10 ** (target_db / 20)

        # Calculate gain
        gain = target_peak / peak

        # Apply gain
        normalized_samples = self.samples * gain

        return AudioSegment(normalized_samples, self.sample_rate, self.channels, self.metadata)

    def split(self, chunk_size_ms: int, overlap_ms: int = 0) -> List["AudioSegment"]:
        """
        Split audio into chunks of specified size.

        Args:
            chunk_size_ms: Chunk size in milliseconds
            overlap_ms: Overlap between chunks in milliseconds

        Returns:
            List of AudioSegment chunks

        Raises:
            ValueError: If chunk_size_ms or overlap_ms are invalid
        """
        if chunk_size_ms <= 0:
            raise ValueError("Chunk size must be positive")
        if overlap_ms < 0:
            raise ValueError("Overlap must be non-negative")
        if overlap_ms >= chunk_size_ms:
            raise ValueError("Overlap must be less than chunk size")

        # Calculate sizes in samples
        chunk_samples = int(self.sample_rate * chunk_size_ms / 1000)
        overlap_samples = int(self.sample_rate * overlap_ms / 1000)
        step_samples = chunk_samples - overlap_samples

        # Create chunks
        chunks = []
        for start in range(0, len(self.samples), step_samples):
            end = start + chunk_samples
            if end > len(self.samples):
                # Pad the last chunk with zeros if needed
                chunk = np.zeros(chunk_samples, dtype=np.float32)
                samples_to_copy = len(self.samples) - start
                chunk[:samples_to_copy] = self.samples[start : start + samples_to_copy]
            else:
                chunk = self.samples[start:end]

            chunks.append(AudioSegment(chunk, self.sample_rate, self.channels, self.metadata))

        return chunks

    def concatenate(self, other: "AudioSegment") -> "AudioSegment":
        """
        Concatenate with another AudioSegment.

        Args:
            other: AudioSegment to concatenate

        Returns:
            Concatenated AudioSegment

        Raises:
            ValueError: If sample rates or channels don't match
        """
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sample rates must match for concatenation")
        if self.channels != other.channels:
            raise ValueError("Channel counts must match for concatenation")

        # Concatenate samples
        concat_samples = np.concatenate([self.samples, other.samples])

        # Merge metadata (keep self's metadata with any new keys from other)
        merged_metadata = self.metadata.copy()
        for key, value in other.metadata.items():
            if key not in merged_metadata:
                merged_metadata[key] = value

        return AudioSegment(concat_samples, self.sample_rate, self.channels, merged_metadata)

    def overlay(
        self, other: "AudioSegment", position_ms: int = 0, gain: float = 1.0
    ) -> "AudioSegment":
        """
        Overlay another AudioSegment on top of this one.

        Args:
            other: AudioSegment to overlay
            position_ms: Position in milliseconds to start the overlay
            gain: Gain to apply to the overlaid audio

        Returns:
            Mixed AudioSegment

        Raises:
            ValueError: If sample rates or channels don't match
        """
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sample rates must match for overlay")
        if self.channels != other.channels:
            raise ValueError("Channel counts must match for overlay")

        # Calculate position in samples
        position_samples = int(self.sample_rate * position_ms / 1000)

        # Create output array (same length as self)
        result = self.samples.copy()

        # Apply overlay
        other_samples = other.samples * gain
        end_pos = min(len(result), position_samples + len(other_samples))
        samples_to_copy = end_pos - position_samples

        if samples_to_copy > 0:
            result[position_samples:end_pos] += other_samples[:samples_to_copy]

        # Clip to [-1.0, 1.0]
        result = np.clip(result, -1.0, 1.0)

        return AudioSegment(result, self.sample_rate, self.channels, self.metadata)

    def apply_gain(self, gain_db: float) -> "AudioSegment":
        """
        Apply gain to the audio.

        Args:
            gain_db: Gain in dB to apply

        Returns:
            Gained AudioSegment
        """
        # Convert dB to linear gain
        gain_linear = 10 ** (gain_db / 20)

        # Apply gain
        gained_samples = self.samples * gain_linear

        # Clip to [-1.0, 1.0]
        gained_samples = np.clip(gained_samples, -1.0, 1.0)

        return AudioSegment(gained_samples, self.sample_rate, self.channels, self.metadata)

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the audio.

        Returns:
            Dictionary of metadata
        """
        metadata = self.metadata.copy()
        metadata.update(
            {
                "duration": self.duration,
                "sample_rate": self.sample_rate,
                "channels": self.channels,
                "n_samples": len(self.samples),
                "min_amplitude": float(np.min(self.samples)),
                "max_amplitude": float(np.max(self.samples)),
                "rms_amplitude": float(np.sqrt(np.mean(self.samples**2))),
            }
        )
        return metadata
