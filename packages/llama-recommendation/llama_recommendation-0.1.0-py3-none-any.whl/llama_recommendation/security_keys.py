"""
Key management utilities for secure encryption.

This module provides utilities for managing cryptographic keys used in
the recommendation system, with a focus on secure key loading and handling.
"""

import base64
import logging
import os
from typing import Optional, Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from llama_recommender.utils.logging import get_logger


def load_encryption_key() -> bytes:
    """
    Load encryption key from environment variable.

    This function loads the encryption key from the LLAMA_ENCRYPTION_KEY
    environment variable. If the key is not set, it raises an error.

    Returns:
        Bytes object containing the encryption key

    Raises:
        ValueError: If the encryption key is not set
    """
    key_str = os.getenv("LLAMA_ENCRYPTION_KEY")
    if not key_str:
        raise ValueError(
            "Encryption key not found. Set the LLAMA_ENCRYPTION_KEY environment variable."
        )

    try:
        # Decode the Base64-encoded key
        key = base64.b64decode(key_str)
        return key
    except Exception as e:
        raise ValueError(f"Failed to decode encryption key: {e}")


def generate_key(length: int = 32) -> Tuple[bytes, str]:
    """
    Generate a new random encryption key.

    Args:
        length: Length of the key in bytes

    Returns:
        Tuple of (key_bytes, base64_encoded_key)
    """
    import secrets

    # Generate random key
    key = secrets.token_bytes(length)

    # Encode key in Base64
    key_b64 = base64.b64encode(key).decode("utf-8")

    return key, key_b64


def derive_key(
    password: str, salt: Optional[bytes] = None, iterations: int = 100000
) -> Tuple[bytes, bytes]:
    """
    Derive an encryption key from a password.

    Args:
        password: Password to derive key from
        salt: Salt for key derivation (if None, a new one is generated)
        iterations: Number of iterations for PBKDF2

    Returns:
        Tuple of (derived_key, salt)
    """
    if salt is None:
        # Generate a random salt
        import os

        salt = os.urandom(16)

    # Set up key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )

    # Derive key
    key = kdf.derive(password.encode())

    return key, salt


def rotate_key(old_key: bytes, new_key: bytes, data_directory: str) -> dict:
    """
    Rotate encryption keys for stored data.

    This function decrypts data with the old key and re-encrypts it with
    the new key. The old key can then be discarded safely.

    Args:
        old_key: Old encryption key
        new_key: New encryption key
        data_directory: Directory containing encrypted data
    """
    import os

    from llama_recommender.security.encryption import decrypt_data, encrypt_data

    logger = get_logger("key_rotation")
    logger.info(f"Starting key rotation for data in {data_directory}")

    # Track statistics
    stats = {"files_processed": 0, "files_skipped": 0, "errors": 0}

    # Process all NPY files
    for root, _, files in os.walk(data_directory):
        for file in files:
            if file.endswith(".npy"):
                file_path = os.path.join(root, file)
                try:
                    # Load encrypted data
                    import numpy as np

                    data = np.load(file_path, allow_pickle=True).item()

                    # Process each item in the dictionary
                    new_data = {}
                    for key, encrypted_value in data.items():
                        # Skip if not encrypted
                        if not isinstance(encrypted_value, dict) or "nonce" not in encrypted_value:
                            new_data[key] = encrypted_value
                            continue

                        # Decrypt with old key
                        decrypted_value = decrypt_data(encrypted_value, key=old_key)

                        # Re-encrypt with new key
                        encrypted_value = encrypt_data(decrypted_value, key=new_key)
                        new_data[key] = encrypted_value

                    # Save updated data
                    np.save(file_path, new_data)
                    stats["files_processed"] += 1

                except Exception as e:
                    logger.error(f"Error rotating keys for {file_path}: {e}")
                    stats["errors"] += 1
                    stats["files_skipped"] += 1

    logger.info(
        f"Key rotation completed: {stats['files_processed']} files processed, {stats['errors']} errors."
    )

    return stats
