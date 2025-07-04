from pydantic import BaseModel, Field, HttpUrl, model_validator
from typing import List, Optional

class CreateProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category: str
    seller_id: str
    images: List[HttpUrl] or List[str]

    @model_validator(mode='after')
    def validate_images(self):
        if not self.images or len(self.images) < 1:
            raise ValueError("At least one image URL is required.")
        return self



