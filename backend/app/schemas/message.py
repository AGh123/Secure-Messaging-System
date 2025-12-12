from pydantic import BaseModel


# -------------------------
# Send message
# -------------------------
class SendMessageRequest(BaseModel):
    receiver: str
    plaintext: str


# -------------------------
# Inbox item (badge UI)
# -------------------------
class InboxItem(BaseModel):
    from_user: str
    count: int


# -------------------------
# Read-once message
# -------------------------
class ReadMessageResponse(BaseModel):
    plaintext: str
