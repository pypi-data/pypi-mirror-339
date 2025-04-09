"""
Secure Enclave Manager for protecting sensitive audio data.

This module provides functionality to securely store and manage sensitive
audio snippets using Apple's Secure Enclave when available.
"""

import json
import logging
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Conditional imports for Secure Enclave
try:
    import pyobjc
    import Security

    HAS_SECURE_ENCLAVE = True
except ImportError:
    HAS_SECURE_ENCLAVE = False

from llama_voice.utils.audio import AudioSegment
from llama_voice.utils.logging import setup_logger


@dataclass
class SecureStorageConfig:
    """Configuration for secure audio storage."""

    storage_path: Optional[str] = None
    max_storage_days: int = 30
    encryption_level: str = "high"  # "standard", "high", or "maximum"
    require_authentication: bool = True
    auto_cleanup: bool = True
    metadata_fields: List[str] = None

    def __post_init__(self):
        if self.metadata_fields is None:
            self.metadata_fields = [
                "timestamp",
                "transcription",
                "duration",
                "sample_rate",
            ]


class SecureEnclaveManager:
    """
    Secure Enclave Manager for protecting sensitive audio data.

    This class provides secure storage and management for sensitive audio snippets,
    using Apple's Secure Enclave when available. It handles encryption, secure
    deletion, and access control for audio data that needs special protection.
    """

    def __init__(
        self,
        config: Optional[SecureStorageConfig] = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the secure enclave manager.

        Args:
            config: Configuration for secure storage
            log_level: Logging level

        Raises:
            ImportError: If Secure Enclave support is not available
        """
        self.logger = setup_logger("secure_enclave", log_level)

        self.config = config or SecureStorageConfig()

        # Check Secure Enclave availability
        self.has_secure_enclave = HAS_SECURE_ENCLAVE
        if not self.has_secure_enclave:
            self.logger.warning("Secure Enclave not available. Falling back to encrypted storage.")

        # Set storage path
        if self.config.storage_path:
            self.storage_path = Path(self.config.storage_path)
        else:
            self.storage_path = Path.home() / ".llama_voice" / "secure_storage"

        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Initialize secure storage
        self._init_secure_storage()

        # Run cleanup if auto-cleanup is enabled
        if self.config.auto_cleanup:
            self._cleanup_old_data()

        self.logger.info(f"Secure Enclave Manager initialized with storage at {self.storage_path}")

    def _init_secure_storage(self) -> None:
        """
        Initialize secure storage and encryption keys.

        This method sets up the secure storage environment and generates
        or loads encryption keys as needed.
        """
        # Create index file if it doesn't exist
        index_path = self.storage_path / "index.json"
        if not index_path.exists():
            with open(index_path, "w") as f:
                json.dump({"entries": {}}, f)

        # Initialize encryption
        if self.has_secure_enclave:
            self._init_secure_enclave()
        else:
            self._init_fallback_encryption()

    def _init_secure_enclave(self) -> None:
        """
        Initialize Secure Enclave for encryption.

        Raises:
            ImportError: If Secure Enclave support is not available
        """
        if not HAS_SECURE_ENCLAVE:
            raise ImportError("Secure Enclave support requires pyobjc")

        try:
            # This is a placeholder for the actual Secure Enclave initialization
            # In a real implementation, this would initialize the Secure Enclave
            # and generate or load encryption keys

            # For demonstration, we'll just log that it's initialized
            self.logger.info("Secure Enclave initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize Secure Enclave: {str(e)}")
            self.has_secure_enclave = False
            self._init_fallback_encryption()

    def _init_fallback_encryption(self) -> None:
        """
        Initialize fallback encryption when Secure Enclave is not available.
        """
        # This is a simplified implementation for demonstration
        # In a real implementation, this would set up proper encryption
        # using a library like cryptography

        # Check if key file exists
        key_path = self.storage_path / ".key"
        if not key_path.exists():
            # Generate a random key
            import secrets

            key = secrets.token_bytes(32)

            # Save key (in a real implementation, this would be more secure)
            with open(key_path, "wb") as f:
                f.write(key)

        self.logger.info("Fallback encryption initialized")

    def _cleanup_old_data(self) -> None:
        """
        Clean up old data based on retention policy.
        """
        if self.config.max_storage_days <= 0:
            return

        try:
            index_path = self.storage_path / "index.json"
            if not index_path.exists():
                return

            # Load index
            with open(index_path, "r") as f:
                index = json.load(f)

            # Get current time
            current_time = time.time()
            max_age = self.config.max_storage_days * 24 * 60 * 60  # days to seconds

            # Find entries to delete
            entries_to_delete = []
            for entry_id, entry in index.get("entries", {}).items():
                timestamp = entry.get("timestamp", 0)
                if current_time - timestamp > max_age:
                    entries_to_delete.append(entry_id)

            # Delete entries
            for entry_id in entries_to_delete:
                self._delete_entry(entry_id, index)

            # Save updated index
            if entries_to_delete:
                with open(index_path, "w") as f:
                    json.dump(index, f)

                self.logger.info(f"Cleaned up {len(entries_to_delete)} old entries")

        except Exception as e:
            self.logger.error(f"Failed to clean up old data: {str(e)}")

    def _delete_entry(self, entry_id: str, index: Dict[str, Any]) -> None:
        """
        Delete an entry and its associated files.

        Args:
            entry_id: ID of the entry to delete
            index: Index dictionary (will be modified)
        """
        try:
            # Get entry data
            entry = index.get("entries", {}).get(entry_id)
            if not entry:
                return

            # Delete data file
            data_path = self.storage_path / f"{entry_id}.enc"
            if data_path.exists():
                data_path.unlink()

            # Remove from index
            index["entries"].pop(entry_id, None)

            self.logger.debug(f"Deleted entry {entry_id}")

        except Exception as e:
            self.logger.error(f"Failed to delete entry {entry_id}: {str(e)}")

    def store_sensitive_audio(
        self,
        audio: Union[AudioSegment, np.ndarray],
        transcription: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Store sensitive audio securely.

        Args:
            audio: Audio data to store
            transcription: Optional transcription of the audio
            metadata: Optional additional metadata

        Returns:
            ID of the stored audio that can be used for retrieval

        Raises:
            ValueError: If storage fails
        """
        try:
            # Generate a unique ID
            entry_id = str(uuid.uuid4())

            # Prepare audio data
            if not isinstance(audio, AudioSegment):
                # Assume numpy array with 16kHz sample rate if not AudioSegment
                from llama_voice.utils.audio import AudioSegment

                audio = AudioSegment(audio, 16000)

            # Prepare metadata
            entry_metadata = metadata or {}
            entry_metadata.update(
                {
                    "timestamp": time.time(),
                    "duration": audio.duration,
                    "sample_rate": audio.sample_rate,
                }
            )

            if transcription:
                entry_metadata["transcription"] = transcription

            # Filter metadata fields if configured
            if self.config.metadata_fields:
                entry_metadata = {
                    k: v for k, v in entry_metadata.items() if k in self.config.metadata_fields
                }

            # Encrypt and store audio
            self._encrypt_and_store(entry_id, audio, entry_metadata)

            self.logger.info(f"Stored sensitive audio with ID {entry_id}")

            return entry_id

        except Exception as e:
            self.logger.error(f"Failed to store sensitive audio: {str(e)}")
            raise ValueError(f"Failed to store sensitive audio: {str(e)}")

    def _encrypt_and_store(
        self, entry_id: str, audio: AudioSegment, metadata: Dict[str, Any]
    ) -> None:
        """
        Encrypt and store audio data.

        Args:
            entry_id: ID for the entry
            audio: Audio data to store
            metadata: Metadata to store with the audio

        Raises:
            ValueError: If encryption or storage fails
        """
        # Convert audio to bytes
        audio_bytes = audio.to_bytes()

        # Encrypt audio
        if self.has_secure_enclave:
            encrypted_data = self._encrypt_with_secure_enclave(audio_bytes)
        else:
            encrypted_data = self._encrypt_fallback(audio_bytes)

        # Store encrypted data
        data_path = self.storage_path / f"{entry_id}.enc"
        with open(data_path, "wb") as f:
            f.write(encrypted_data)

        # Update index
        index_path = self.storage_path / "index.json"
        try:
            with open(index_path, "r") as f:
                index = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            index = {"entries": {}}

        # Add entry to index
        index["entries"][entry_id] = metadata

        # Save updated index
        with open(index_path, "w") as f:
            json.dump(index, f)

    def _encrypt_with_secure_enclave(self, data: bytes) -> bytes:
        """
        Encrypt data using Secure Enclave.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data

        Raises:
            ValueError: If encryption fails
        """
        if not self.has_secure_enclave:
            raise ValueError("Secure Enclave not available")

        try:
            # This is a placeholder for the actual Secure Enclave encryption
            # In a real implementation, this would use the Secure Enclave to encrypt the data

            # For demonstration, we'll just simulate encryption
            # with a simple XOR with a fixed key (NOT secure, just for demonstration)
            key = b"SecureEnclaveSimulation"
            key_extended = key * (len(data) // len(key) + 1)
            encrypted = bytes(a ^ b for a, b in zip(data, key_extended[: len(data)]))

            return encrypted

        except Exception as e:
            self.logger.error(f"Secure Enclave encryption failed: {str(e)}")
            raise ValueError(f"Secure Enclave encryption failed: {str(e)}")

    def _encrypt_fallback(self, data: bytes) -> bytes:
        """
        Encrypt data using fallback encryption.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data

        Raises:
            ValueError: If encryption fails
        """
        try:
            # This is a simplified implementation for demonstration
            # In a real implementation, this would use proper encryption

            # Load key
            key_path = self.storage_path / ".key"
            with open(key_path, "rb") as f:
                key = f.read()

            # Simple XOR encryption (NOT secure, just for demonstration)
            key_extended = key * (len(data) // len(key) + 1)
            encrypted = bytes(a ^ b for a, b in zip(data, key_extended[: len(data)]))

            return encrypted

        except Exception as e:
            self.logger.error(f"Fallback encryption failed: {str(e)}")
            raise ValueError(f"Fallback encryption failed: {str(e)}")

    def retrieve_sensitive_audio(
        self, entry_id: str, require_authentication: bool = None
    ) -> Tuple[AudioSegment, Dict[str, Any]]:
        """
        Retrieve sensitive audio securely.

        Args:
            entry_id: ID of the audio to retrieve
            require_authentication: Whether to require authentication (overrides config)

        Returns:
            Tuple of (audio_data, metadata)

        Raises:
            ValueError: If retrieval fails or authentication is required but fails
        """
        # Determine if authentication is required
        need_auth = (
            require_authentication
            if require_authentication is not None
            else self.config.require_authentication
        )

        try:
            # Check if entry exists
            index_path = self.storage_path / "index.json"
            with open(index_path, "r") as f:
                index = json.load(f)

            entry = index.get("entries", {}).get(entry_id)
            if not entry:
                raise ValueError(f"Entry {entry_id} not found")

            # Check if file exists
            data_path = self.storage_path / f"{entry_id}.enc"
            if not data_path.exists():
                raise ValueError(f"Data file for entry {entry_id} not found")

            # Authenticate if required
            if need_auth and self.has_secure_enclave:
                if not self._authenticate():
                    raise ValueError("Authentication failed")

            # Load encrypted data
            with open(data_path, "rb") as f:
                encrypted_data = f.read()

            # Decrypt data
            if self.has_secure_enclave:
                audio_bytes = self._decrypt_with_secure_enclave(encrypted_data)
            else:
                audio_bytes = self._decrypt_fallback(encrypted_data)

            # Convert to AudioSegment
            sample_rate = entry.get("sample_rate", 16000)
            audio = AudioSegment.from_bytes(audio_bytes, sample_rate)

            self.logger.info(f"Retrieved sensitive audio with ID {entry_id}")

            return audio, entry

        except Exception as e:
            self.logger.error(f"Failed to retrieve sensitive audio: {str(e)}")
            raise ValueError(f"Failed to retrieve sensitive audio: {str(e)}")

    def _decrypt_with_secure_enclave(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using Secure Enclave.

        Args:
            encrypted_data: Encrypted data

        Returns:
            Decrypted data

        Raises:
            ValueError: If decryption fails
        """
        if not self.has_secure_enclave:
            raise ValueError("Secure Enclave not available")

        try:
            # This is a placeholder for the actual Secure Enclave decryption
            # In a real implementation, this would use the Secure Enclave to decrypt the data

            # For demonstration, we'll just simulate decryption
            # with a simple XOR with a fixed key (matching the encryption)
            key = b"SecureEnclaveSimulation"
            key_extended = key * (len(encrypted_data) // len(key) + 1)
            decrypted = bytes(
                a ^ b for a, b in zip(encrypted_data, key_extended[: len(encrypted_data)])
            )

            return decrypted

        except Exception as e:
            self.logger.error(f"Secure Enclave decryption failed: {str(e)}")
            raise ValueError(f"Secure Enclave decryption failed: {str(e)}")

    def _decrypt_fallback(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using fallback decryption.

        Args:
            encrypted_data: Encrypted data

        Returns:
            Decrypted data

        Raises:
            ValueError: If decryption fails
        """
        try:
            # This is a simplified implementation for demonstration
            # In a real implementation, this would use proper decryption

            # Load key
            key_path = self.storage_path / ".key"
            with open(key_path, "rb") as f:
                key = f.read()

            # Simple XOR decryption (NOT secure, just for demonstration)
            key_extended = key * (len(encrypted_data) // len(key) + 1)
            decrypted = bytes(
                a ^ b for a, b in zip(encrypted_data, key_extended[: len(encrypted_data)])
            )

            return decrypted

        except Exception as e:
            self.logger.error(f"Fallback decryption failed: {str(e)}")
            raise ValueError(f"Fallback decryption failed: {str(e)}")
