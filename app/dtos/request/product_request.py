from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    stock : int = Field(ge=6)
    seller_id: str