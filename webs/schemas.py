from pydantic import BaseModel


class WebhookPayload(BaseModel):
    event: str
    data: dict