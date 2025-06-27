from datetime import datetime
from bson import ObjectId
from flask import current_app


class Product:
    def __init__(self, name, description, price, category, stock, seller_id, images_url=None,is_active=True, created_at=None, updated_at=None):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock = stock
        self.seller_id = ObjectId(seller_id)
        self.images_url = images
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'stock': self.stock,
            'seller_id': self.seller_id,
            'images_url': self.images_url,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    @staticmethod
    def from_dict(data):
        return Product(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            category=data.get('category'),
            stock=data.get('stock'),
            seller_id=data.get('seller_id'),
            images_url=data.get('images_url'),
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