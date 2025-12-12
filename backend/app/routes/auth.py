from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.crypto.rsa import generate_rsa_keypair, serialize_public_key
from app.routes.auth_utils import hash_password, verify_password
from app.routes.session_utils import create_session, delete_session

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
# Register
# -------------------------
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    password_hash = hash_password(data.password)

    # Generate RSA key pair (identity)
    _, public_key = generate_rsa_keypair()
    public_key_bytes = serialize_public_key(public_key)

    user = User(
        username=data.username,
        password_hash=password_hash,
        rsa_public_key=public_key_bytes,
    )

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}


# -------------------------
# Login
# -------------------------
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create DB-backed session token
    token = create_session(db, user.id)

    return {
        "message": "Login successful",
        "token": token,
    }


# -------------------------
# Logout
# -------------------------
@router.post("/logout")
def logout(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    delete_session(db, authorization)
    return {"message": "Logged out successfully"}
