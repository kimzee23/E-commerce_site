from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductTrackerResponse(BaseModel):
    product_id: str
    views: int
    purchases: int
    last_viewed: Optional[datetime]
    last_purchase: Optional[datetime]

