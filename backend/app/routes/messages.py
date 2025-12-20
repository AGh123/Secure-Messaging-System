from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.models.message import Message
from app.models.user import User
from app.schemas.message import SendMessageRequest, InboxItem, ReadMessageResponse
from app.crypto.dh import generate_ephemeral_keypair, derive_shared_key
from app.crypto.aes_gcm import encrypt, decrypt
from app.routes.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send")
def send_message(
    data: SendMessageRequest,
    db: Session = Depends(get_db),
    sender: User = Depends(get_current_user),
):
    receiver = db.query(User).filter(User.username == data.receiver).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    s_priv, _ = generate_ephemeral_keypair()
    r_priv, r_pub = generate_ephemeral_keypair()
    aes_key = derive_shared_key(s_priv, r_pub)

    nonce, ciphertext = encrypt(aes_key, data.plaintext.encode())

    msg = Message(
        sender=sender.username,
        receiver=receiver.username,
        ciphertext=ciphertext,
        nonce=nonce,
        aes_key=aes_key,
    )

    db.add(msg)
    db.commit()

    return {"message": "Message sent"}

@router.get("/inbox", response_model=list[InboxItem])
def inbox(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = (
        db.query(Message.sender)
        .filter(Message.receiver == user.username)
        .all()
    )

    inbox = {}
    for (sender,) in rows:
        inbox[sender] = inbox.get(sender, 0) + 1

    return [
        {"from_user": sender, "count": count}
        for sender, count in inbox.items()
    ]

class OpenMessageRequest(BaseModel):
    from_user: str


@router.post("/open", response_model=ReadMessageResponse)
def open_message(
    data: OpenMessageRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    msg = (
        db.query(Message)
        .filter(
            Message.receiver == user.username,
            Message.sender == data.from_user,
        )
        .first()
    )

    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    plaintext = decrypt(
        msg.aes_key,
        msg.nonce,
        msg.ciphertext,
    ).decode()

    db.delete(msg)
    db.commit()

    return {"plaintext": plaintext}
