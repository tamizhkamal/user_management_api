from datetime import datetime
from pydantic import BaseModel


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

# Define a Pydantic model to parse incoming webhook data
class WebhookPayload(BaseModel):
    event: str
    data: dict  # Adjust according to your expected data structure
