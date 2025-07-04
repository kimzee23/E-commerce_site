from datetime import datetime, timezone
from typing import List
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
    created_at:  datetime
    updated_at:  datetime

    @model_validator(mode='after')
    def validate_images(self):
        if not self.images_url or len(self.images_url) < 1:
            raise ValueError("At least one image URL is required.")
        return self

    @classmethod
    def from_model(cls, model):
        return cls(
            id=str(getattr(model, "_id", model.id)),
            name=model.name,
            description=model.description,
            price=model.price,
            category=model.category,
            stock_quantity=model.stock_quantity,
            seller_id=str(model.seller_id),
            images_url=model.images_url,
            is_active=model.is_active,
            created_at=model.created_at.isoformat(),
            updated_at=model.updated_at.isoformat(),

        )
