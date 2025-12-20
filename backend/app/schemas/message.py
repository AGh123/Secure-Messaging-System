from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    receiver: str
    plaintext: str

class InboxItem(BaseModel):
    from_user: str
    count: int

class ReadMessageResponse(BaseModel):
    plaintext: str
