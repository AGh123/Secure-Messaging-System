from fastapi import FastAPI

app = FastAPI(
    title="CipherCapsule API",
    description="Ephemeral-key self-destructing secure messaging system",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"status": "CipherCapsule backend running"}
