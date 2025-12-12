from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    sender: str
    receiver: str
    plaintext: str


class SendMessageResponse(BaseModel):
    message_id: int


class ReadMessageResponse(BaseModel):
    plaintext: str
