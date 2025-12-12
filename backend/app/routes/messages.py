from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.message import Message
from app.models.user import User
from app.schemas.message import (
    SendMessageRequest,
    SendMessageResponse,
    ReadMessageResponse,
)
from app.crypto.dh import generate_ephemeral_keypair, derive_shared_key
from app.crypto.aes_gcm import encrypt, decrypt
from app.routes.session_utils import get_user_id_from_token

router = APIRouter()


# -------------------------
# Database dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Auth dependency
# -------------------------
def require_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
) -> User:
    user_id = get_user_id_from_token(db, authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return user


# -------------------------
# Send encrypted message
# -------------------------
@router.post("/send", response_model=SendMessageResponse)
def send_message(
    data: SendMessageRequest,
    db: Session = Depends(get_db),
    sender: User = Depends(require_user),
):
    receiver = db.query(User).filter(User.username == data.receiver).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Ephemeral Diffie–Hellman → one-time AES key
    s_priv, s_pub = generate_ephemeral_keypair()
    r_priv, r_pub = generate_ephemeral_keypair()
    aes_key = derive_shared_key(s_priv, r_pub)

    # Encrypt message content
    nonce, ciphertext = encrypt(aes_key, data.plaintext.encode())

    # Encrypt metadata (sender + receiver)
    _, enc_sender = encrypt(aes_key, sender.username.encode())
    _, enc_receiver = encrypt(aes_key, receiver.username.encode())

    msg = Message(
        ciphertext=ciphertext,
        nonce=nonce,
        enc_sender=enc_sender,
        enc_receiver=enc_receiver,
        aes_key=aes_key,
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return {"message_id": msg.id}


# -------------------------
# Read & self-destruct message
# -------------------------
@router.get("/{message_id}", response_model=ReadMessageResponse)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    # Decrypt receiver metadata
    receiver = decrypt(
        msg.aes_key,
        msg.nonce,
        msg.enc_receiver,
    ).decode()

    if receiver != user.username:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Decrypt message
    plaintext = decrypt(
        msg.aes_key,
        msg.nonce,
        msg.ciphertext,
    ).decode()

    # 🔥 Self-destruct (message + key)
    db.delete(msg)
    db.commit()

    return {"plaintext": plaintext}
