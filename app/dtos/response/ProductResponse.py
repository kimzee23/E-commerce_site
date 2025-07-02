from pydantic.v1 import root_validator
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, model_validator


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    stock_quantity: int
    seller_id: str
    images_url: List[HttpUrl]
    is_active: bool
    created_at: str
    updated_at: str

    @model_validator(mode='after')
    def validate_images(self):
        if not self.images or len(self.images) < 1:
            raise ValueError("At least one image URL is required.")
        return self
