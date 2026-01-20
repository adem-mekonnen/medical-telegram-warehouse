from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    product_name: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    post_count: int

class MessageResponse(BaseModel):
    message_id: int
    text: str
    views: int

class VisualStats(BaseModel):
    category: str
    count: int