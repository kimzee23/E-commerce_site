import traceback
from datetime import datetime, timezone

from bson import ObjectId
from flask import current_app
from pydantic import BaseModel


class Product:
    def __init__(self, name, description, price, category, stock_quantity, seller_id,images_url=None, is_active=True, created_at=None, updated_at=None, id=None):
        self.id = id or ObjectId()
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        self.seller_id = ObjectId(seller_id)
        self.images_url = images_url or []
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "stock_quantity": self.stock_quantity,
            "seller_id": self.seller_id,
            "images_url": [str(url) for url in self.images_url],
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        if isinstance(data, BaseModel):
            data = data.model_dump()
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data)}")
        images_raw = data.get('images_url') or data.get('images') or []
        images_url = [str(url) for url in images_raw]

        return Product(
            id=data.get('_id'),
            name=data['name'],
            description=data['description'],
            price=data['price'],
            category=data['category'],
            stock_quantity=data['stock_quantity'],
            seller_id=data['seller_id'],
            images_url=images_url,
            is_active=data.get('is_active', True),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    @staticmethod
    def update_product(product_id, seller_id, updates):
        db = current_app.mongo.db
        result = db.products.update_one(
            {"_id": ObjectId(product_id), "seller_id": ObjectId(seller_id)},
            {"$set": updates}
        )
        return result.modified_count > 0