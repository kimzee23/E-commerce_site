from pydantic import BaseModel, Field, HttpUrl, root_validator
from typing import List

class CreateProductRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)
    price: float = Field(..., gt=0)
    category: str
    stock_quantity: int = Field(..., ge=0)
    images: List[HttpUrl]
    seller_id: str

    @root_validator
    def validate_images(cls, values):
        images = values.get("images")
        if not images or len(images) < 1:
            raise ValueError("At least one image URL is required.")
        return values
