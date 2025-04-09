"""
Security components for llama_backup.

This module provides security-related functionality including encryption,
hashing, key management, and blockchain verification.
"""

import base64
import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Optional

# Configure logging
logger = logging.getLogger("llama_backup.security")

# Third-party dependencies
try:
    import mlx.core as mx
    import numpy as np
    import web3
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    logger.warning(
        "Some security dependencies are missing. Please install them using: "
        "pip install -r requirements.txt"
    )


class SecurityManager:
    """Manages encryption, hashing, and key management for secure backups."""

    def __init__(self, key_path: Optional[str] = None):
        """Initialize the security manager.

        Args:
            key_path: Optional path to key file, if not provided will use environment variables
        """
        self.key_path = key_path
        self._encryption_key = self._load_encryption_key()
        self._fernet = Fernet(self._encryption_key)

    def _load_encryption_key(self) -> bytes:
        """Load or generate encryption key.

        Returns:
            bytes: The encryption key
        """
        if self.key_path and os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read()
        elif "LLAMA_BACKUP_KEY" in os.environ:
            key = os.environ["LLAMA_BACKUP_KEY"]
            if len(key) < 32:
                logger.warning("Encryption key from environment is too short, padding")
                key = key.ljust(32, "X")
            return base64.urlsafe_b64encode(key[:32].encode())
        else:
            # Generate a new key
            logger.warning("No encryption key found, generating a new one")
            key = Fernet.generate_key()
            if self.key_path:
                with open(self.key_path, "wb") as f:
                    f.write(key)
            return key

    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data using Fernet symmetric encryption.

        Args:
            data: The data to encrypt

        Returns:
            bytes: Encrypted data
        """
        return self._fernet.encrypt(data)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt Fernet-encrypted data.

        Args:
            encrypted_data: The encrypted data

        Returns:
            bytes: Decrypted data
        """
        return self._fernet.decrypt(encrypted_data)

    def hash_data(self, data: bytes) -> str:
        """Generate a SHA-256 hash of data.

        Args:
            data: The data to hash

        Returns:
            str: Hexadecimal hash digest
        """
        return hashlib.sha256(data).hexdigest()

    def mlx_encrypt(self, data: bytes) -> bytes:
        """Advanced encryption using MLX acceleration.

        Args:
            data: The data to encrypt

        Returns:
            bytes: MLX-encrypted data
        """
        # Convert data to MLX array for accelerated processing
        data_array = np.frombuffer(data, dtype=np.uint8)
        mx_array = mx.array(data_array)

        # Generate a random key for this encryption
        key = os.urandom(32)
        iv = os.urandom(16)

        # Encrypt with AES
        # (In a real implementation, we would use MLX optimized AES)
        # Here we're mocking this with standard cryptography
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        # Pad the data to a multiple of 16 bytes (AES block size)
        padded_data = self._pad_data(data)
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Include the key and IV in the result (would be encrypted with a master key in production)
        result = base64.b64encode(key + iv + encrypted)
        return result

    def mlx_decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt MLX-encrypted data.

        Args:
            encrypted_data: The encrypted data

        Returns:
            bytes: Decrypted data
        """
        # Decode the base64
        decoded = base64.b64decode(encrypted_data)

        # Extract the key, IV, and ciphertext
        key = decoded[:32]
        iv = decoded[32:48]
        ciphertext = decoded[48:]

        # Decrypt with AES
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        return self._unpad_data(decrypted_padded)

    def _pad_data(self, data: bytes) -> bytes:
        """PKCS7 padding for AES encryption."""
        block_size = 16
        padding_size = block_size - (len(data) % block_size)
        padding = bytes([padding_size]) * padding_size
        return data + padding

    def _unpad_data(self, padded_data: bytes) -> bytes:
        """Remove PKCS7 padding."""
        padding_size = padded_data[-1]
        return padded_data[:-padding_size]

    def verify_blockchain_hash(self, data: bytes, receipt: str) -> bool:
        """Verify data integrity using blockchain receipt.

        Args:
            data: The data to verify
            receipt: Blockchain receipt containing the stored hash

        Returns:
            bool: True if verification succeeds
        """
        try:
            # Parse the receipt
            receipt_data = json.loads(receipt)
            stored_hash = receipt_data.get("hash")

            if not stored_hash:
                logger.error("Invalid receipt format, missing hash")
                return False

            # Calculate the hash of the current data
            current_hash = self.hash_data(data)

            # Compare hashes
            return stored_hash == current_hash
        except Exception as e:
            logger.error(f"Blockchain verification failed: {str(e)}")
            return False


class BlockchainVerifier:
    """Handles blockchain verification of backup integrity."""

    def __init__(self, blockchain_url: Optional[str] = None):
        """Initialize the blockchain verifier.

        Args:
            blockchain_url: URL of the blockchain node to connect to
        """
        self.blockchain_url = blockchain_url or os.environ.get("LLAMA_BACKUP_BLOCKCHAIN_URL")
        self.web3 = None
        self._initialize_web3()

    def _initialize_web3(self):
        """Initialize the Web3 connection if a blockchain URL is provided."""
        if self.blockchain_url:
            try:
                self.web3 = web3.Web3(web3.Web3.HTTPProvider(self.blockchain_url))
                logger.info(f"Connected to blockchain: {self.web3.is_connected()}")
            except Exception as e:
                logger.warning(f"Failed to initialize blockchain connection: {str(e)}")

    def create_hash_receipt(self, chunk_id: str, hash_value: str) -> str:
        """Create a receipt for a hash without actually writing to blockchain.

        In a production environment, this would write to a blockchain.
        For this implementation, we create a mock receipt.

        Args:
            chunk_id: ID of the chunk
            hash_value: SHA-256 hash of the chunk

        Returns:
            str: JSON receipt as a string
        """
        receipt = {
            "chunk_id": chunk_id,
            "hash": hash_value,
            "timestamp": datetime.now().isoformat(),
            "verified": True,
            "blockchain_tx": f"0x{os.urandom(32).hex()}",  # Mock transaction ID
        }
        return json.dumps(receipt)

    def verify_hash_receipt(self, receipt: str, hash_value: str) -> bool:
        """Verify a hash receipt.

        Args:
            receipt: JSON receipt as a string
            hash_value: Hash to verify against

        Returns:
            bool: True if verification succeeds
        """
        try:
            receipt_data = json.loads(receipt)
            return receipt_data.get("hash") == hash_value
        except Exception as e:
            logger.error(f"Receipt verification failed: {str(e)}")
            return False
