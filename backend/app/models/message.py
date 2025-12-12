from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    # Plain metadata (needed for inbox & routing)
    sender = Column(String, nullable=False, index=True)
    receiver = Column(String, nullable=False, index=True)

    # Encrypted payload
    ciphertext = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)

    # One-time session key (deleted after read)
    aes_key = Column(LargeBinary, nullable=False)
