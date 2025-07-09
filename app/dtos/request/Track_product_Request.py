from pydantic import BaseModel


class TrackProductRequest(BaseModel):
    product_id: str

