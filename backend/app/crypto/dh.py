from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def generate_ephemeral_keypair():
    """
    Generates an ephemeral ECDH key pair.
    """
    private_key = ec.generate_private_key(
        ec.SECP256R1(),
        default_backend(),
    )
    public_key = private_key.public_key()
    return private_key, public_key


def derive_shared_key(
    private_key,
    peer_public_key,
    salt: bytes = None,
    info: bytes = b"ciphercapsule-message-key",
) -> bytes:
    """
    Derives a 256-bit AES key using ECDH + HKDF.
    """
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit AES key
        salt=salt,
        info=info,
        backend=default_backend(),
    )

    return hkdf.derive(shared_secret)
