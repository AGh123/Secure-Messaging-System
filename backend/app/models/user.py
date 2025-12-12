from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    rsa_public_key = Column(LargeBinary, nullable=False)
