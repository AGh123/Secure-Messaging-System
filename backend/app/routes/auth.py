from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.session import Session as UserSession
from app.schemas.auth import RegisterRequest, LoginRequest
from app.crypto.rsa import generate_rsa_keypair, serialize_public_key
from app.routes.auth_utils import hash_password, verify_password
from app.routes.session_utils import create_session, delete_session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")

    session = (
        db.query(UserSession)
        .filter(UserSession.token == authorization)
        .first()
    )

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    password_hash = hash_password(data.password)

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


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_session(db, user.id)

    return {"token": token}

@router.post("/logout")
def logout(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not authorization:
        return {"message": "Already logged out"}

    delete_session(db, authorization)
    return {"message": "Logged out successfully"}

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}

@router.get("/users")
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User.username)
        .filter(User.username != current_user.username)
        .all()
    )
    return [u[0] for u in users]
