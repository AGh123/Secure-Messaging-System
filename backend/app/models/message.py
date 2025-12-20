from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    sender = Column(String, nullable=False, index=True)
    receiver = Column(String, nullable=False, index=True)

    ciphertext = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)

    aes_key = Column(LargeBinary, nullable=False)
