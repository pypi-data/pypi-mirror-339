"""
Encryption utilities for protecting sensitive data.

This module provides encryption and decryption functions for securing
sensitive data in the recommendation system, including embeddings and
user information.
"""

import base64
import os
from typing import Any, Dict, List, Optional

import numpy as np
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from llama_recommender.security.keys import load_encryption_key
from llama_recommender.utils.logging import get_logger


def encrypt_data(data: Any, key: Optional[bytes] = None) -> Dict[str, Any]:
    """
    Encrypt data using AES-GCM.

    Args:
        data: Data to encrypt (can be a NumPy array or any serializable object)
        key: Encryption key (if None, loaded from environment)

    Returns:
        Dictionary with encrypted data and metadata
    """
    logger = get_logger("encryption")

    # Load key if not provided
    if key is None:
        key = load_encryption_key()

    # Generate a random nonce
    nonce = os.urandom(12)  # 96 bits as recommended for AES-GCM

    # Serialize data
    if isinstance(data, np.ndarray):
        # Convert NumPy array to bytes
        serialized = data.tobytes()
        shape = data.shape
        dtype = str(data.dtype)
        is_numpy = True
    else:
        # Use pickle for other data types
        import pickle

        serialized = pickle.dumps(data)
        shape = None
        dtype = None
        is_numpy = False

    try:
        # Create cipher
        cipher = AESGCM(key)

        # Encrypt data
        encrypted = cipher.encrypt(nonce, serialized, None)

        # Create metadata
        result = {
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "encrypted": base64.b64encode(encrypted).decode("utf-8"),
            "is_numpy": is_numpy,
        }

        # Add NumPy metadata if applicable
        if is_numpy:
            result["shape"] = shape
            result["dtype"] = dtype

        return result

    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise


def decrypt_data(encrypted_data: Dict[str, Any], key: Optional[bytes] = None) -> Any:
    """
    Decrypt data using AES-GCM.

    Args:
        encrypted_data: Dictionary with encrypted data and metadata
        key: Encryption key (if None, loaded from environment)

    Returns:
        Decrypted data
    """
    logger = get_logger("encryption")

    # Load key if not provided
    if key is None:
        key = load_encryption_key()

    try:
        # Extract metadata
        nonce = base64.b64decode(encrypted_data["nonce"])
        encrypted = base64.b64decode(encrypted_data["encrypted"])
        is_numpy = encrypted_data.get("is_numpy", False)

        # Create cipher
        cipher = AESGCM(key)

        # Decrypt data
        decrypted = cipher.decrypt(nonce, encrypted, None)

        # Deserialize data
        if is_numpy:
            # Convert bytes back to NumPy array
            shape = encrypted_data["shape"]
            dtype = encrypted_data["dtype"]
            array = np.frombuffer(decrypted, dtype=dtype)
            if shape is not None and len(shape) > 1:
                array = array.reshape(shape)
            return array
        else:
            # Use pickle for other data types
            import pickle

            return pickle.loads(decrypted)

    except InvalidTag:
        logger.error(
            "Decryption error: Invalid authentication tag - data may be corrupted or tampered with"
        )
        raise ValueError("Data authentication failed - possible tampering detected")

    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise


def encrypt_file(
    input_path: str, output_path: Optional[str] = None, key: Optional[bytes] = None
) -> str:
    """
    Encrypt a file using AES-GCM.

    Args:
        input_path: Path to the file to encrypt
        output_path: Path to save the encrypted file (if None, appends '.enc')
        key: Encryption key (if None, loaded from environment)

    Returns:
        Path to the encrypted file
    """
    logger = get_logger("encryption")

    # Set output path if not provided
    if output_path is None:
        output_path = input_path + ".enc"

    # Load key if not provided
    if key is None:
        key = load_encryption_key()

    try:
        # Read input file
        with open(input_path, "rb") as f:
            data = f.read()

        # Generate a random nonce
        nonce = os.urandom(12)  # 96 bits as recommended for AES-GCM

        # Create cipher
        cipher = AESGCM(key)

        # Encrypt data
        encrypted = cipher.encrypt(nonce, data, None)

        # Write encrypted file with nonce at the beginning
        with open(output_path, "wb") as f:
            f.write(nonce)
            f.write(encrypted)

        logger.info(f"Encrypted {input_path} to {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"File encryption error: {e}")
        raise


def decrypt_file(
    input_path: str, output_path: Optional[str] = None, key: Optional[bytes] = None
) -> str:
    """
    Decrypt a file encrypted with AES-GCM.

    Args:
        input_path: Path to the encrypted file
        output_path: Path to save the decrypted file (if None, removes '.enc')
        key: Encryption key (if None, loaded from environment)

    Returns:
        Path to the decrypted file
    """
    logger = get_logger("encryption")

    # Set output path if not provided
    if output_path is None:
        if input_path.endswith(".enc"):
            output_path = input_path[:-4]
        else:
            output_path = input_path + ".dec"

    # Load key if not provided
    if key is None:
        key = load_encryption_key()

    try:
        # Read encrypted file
        with open(input_path, "rb") as f:
            # Read the first 12 bytes as nonce
            nonce = f.read(12)
            # Read the rest as encrypted data
            encrypted = f.read()

        # Create cipher
        cipher = AESGCM(key)

        # Decrypt data
        decrypted = cipher.decrypt(nonce, encrypted, None)

        # Write decrypted file
        with open(output_path, "wb") as f:
            f.write(decrypted)

        logger.info(f"Decrypted {input_path} to {output_path}")
        return output_path

    except InvalidTag:
        logger.error(
            "File decryption error: Invalid authentication tag - file may be corrupted or tampered with"
        )
        raise ValueError("File authentication failed - possible tampering detected")

    except Exception as e:
        logger.error(f"File decryption error: {e}")
        raise


def encrypt_dataframe(
    df: "pd.DataFrame", columns: List[str], key: Optional[bytes] = None
) -> "pd.DataFrame":
    """
    Encrypt specific columns in a pandas DataFrame.

    Args:
        df: pandas DataFrame to encrypt
        columns: List of column names to encrypt
        key: Encryption key (if None, loaded from environment)

    Returns:
        DataFrame with encrypted columns
    """

    # Make a copy to avoid modifying the original
    encrypted_df = df.copy()

    # Load key if not provided
    if key is None:
        key = load_encryption_key()

    # Encrypt each specified column
    for col in columns:
        if col in encrypted_df.columns:
            encrypted_df[col] = encrypted_df[col].apply(lambda x: encrypt_data(x, key))

    # Add metadata about encrypted columns
    encrypted_df.attrs["encrypted_columns"] = columns

    return encrypted_df


def decrypt_dataframe(
    df: "pd.DataFrame", columns: Optional[List[str]] = None, key: Optional[bytes] = None
) -> "pd.DataFrame":
    """
    Decrypt columns in a pandas DataFrame.

    Args:
        df: pandas DataFrame with encrypted columns
        columns: List of column names to decrypt (if None, uses metadata)
        key: Encryption key (if None, loaded from environment)

    Returns:
        DataFrame with decrypted columns
    """

    # Make a copy to avoid modifying the original
    decrypted_df = df.copy()

    # Load key if not provided
    if key is None:
        key = load_encryption_key()

    # Determine which columns to decrypt
    if columns is None:
        columns = decrypted_df.attrs.get("encrypted_columns", [])

    # Decrypt each specified column
    for col in columns:
        if col in decrypted_df.columns:
            decrypted_df[col] = decrypted_df[col].apply(
                lambda x: (decrypt_data(x, key) if isinstance(x, dict) and "nonce" in x else x)
            )

    # Update metadata
    remaining = [c for c in decrypted_df.attrs.get("encrypted_columns", []) if c not in columns]
    if remaining:
        decrypted_df.attrs["encrypted_columns"] = remaining
    else:
        # Remove metadata if all columns are decrypted
        if "encrypted_columns" in decrypted_df.attrs:
            del decrypted_df.attrs["encrypted_columns"]

    return decrypted_df
