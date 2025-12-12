from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Import models so SQLAlchemy registers tables
from app.models import user, message, session

from app.routes import auth, messages

app = FastAPI(
    title="CipherCapsule API",
    description="Ephemeral-key self-destructing secure messaging system",
    version="1.0.0",
)

# ✅ CORS MUST be added immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])

@app.get("/")
def root():
    return {"status": "CipherCapsule backend running"}
