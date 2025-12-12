import secrets
from sqlalchemy.orm import Session

from app.models.session import Session as UserSession


def create_session(db: Session, user_id: int) -> str:
    """
    Create a new session token for a user.
    """
    token = secrets.token_hex(32)

    session = UserSession(
        token=token,
        user_id=user_id,
    )

    db.add(session)
    db.commit()

    return token


def get_user_id_from_token(db: Session, token: str) -> int | None:
    """
    Resolve user_id from a session token.
    """
    session = (
        db.query(UserSession)
        .filter(UserSession.token == token)
        .first()
    )

    return session.user_id if session else None


def delete_session(db: Session, token: str) -> None:
    """
    Destroy a session token (logout).
    """
    session = (
        db.query(UserSession)
        .filter(UserSession.token == token)
        .first()
    )

    if session:
        db.delete(session)
        db.commit()
