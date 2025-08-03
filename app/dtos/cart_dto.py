from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class CartItemDTO:
    item_id: str
    product_id: str
    quantity: int
    price_at_addition: float
    attributes: Optional[dict]
    added_at: datetime

@dataclass
class CartDTO:
    cart_id: str
    user_id: Optional[str]
    status: str
    subtotal: float
    tax_amount: float
    shipping_amount: float
    total: float
    currency: str
    items: List[CartItemDTO]
    created_at: datetime
    updated_at: datetime