from datetime import datetime
from typing import List
from pydantic import BaseModel,HttpUrl
from pydantic.v1 import root_validator


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    description: str
    stock_quantity: int
    category: str
    images: List[HttpUrl]
    seller_id : str
    status: str
    created_at: datetime
    updated_at: datetime | None = None

    @root_validator
    def check_image_is_not_empty(cls, values):
        image = values['images']
        if not image or len(image) < 1 :
            raise ValueError('Image must have at least one image')
        return values