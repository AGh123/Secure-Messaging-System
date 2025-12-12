from sqlalchemy import Column, Integer, LargeBinary
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    # Encrypted payload
    ciphertext = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)

    # Encrypted metadata
    enc_sender = Column(LargeBinary, nullable=False)
    enc_receiver = Column(LargeBinary, nullable=False)

    # One-time session key (deleted after read)
    aes_key = Column(LargeBinary, nullable=False)
