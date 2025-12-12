from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from typing import Tuple, Optional


NONCE_SIZE = 12


def encrypt(
    key: bytes,
    plaintext: bytes,
    associated_data: Optional[bytes] = None,
) -> Tuple[bytes, bytes]:
    """
    Encrypts plaintext using AES-256-GCM.

    Returns:
        nonce, ciphertext
    """
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")

    nonce = os.urandom(NONCE_SIZE)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(
        nonce=nonce,
        data=plaintext,
        associated_data=associated_data,
    )

    return nonce, ciphertext


def decrypt(
    key: bytes,
    nonce: bytes,
    ciphertext: bytes,
    associated_data: Optional[bytes] = None,
) -> bytes:
    """
    Decrypts AES-256-GCM ciphertext.

    Raises:
        InvalidTag if authentication fails
    """
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")

    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        nonce=nonce,
        data=ciphertext,
        associated_data=associated_data,
    )

    return plaintext
