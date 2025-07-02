from bson import ObjectId
from flask import current_app

from app.dtos.request.product_request import CreateProductRequest
from app.models.product_model import Product


class ProductService:
    @staticmethod
    def create_product(product_data: CreateProductRequest):
        data = product_data.model_dump()
        product = Product.from_dict(data)
        db = current_app.mongo.db
        result = db.products.insert_one(product.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def get_all_products():
        db = current_app.mongo.db
        products = db.products.find()
        return [Product.from_dict(p).__dict__ for p in products]

    @staticmethod
    def get_product_by_id(product_id):
        db = current_app.mongo.db
        product = db.products.find_one({"_id": ObjectId(product_id)})
        return Product.from_dict(product) if product else None

    @staticmethod
    def get_products_by_seller(seller_id):
        db = current_app.mongo.db
        products = db.products.find({"seller_id": ObjectId(seller_id)})
        return [Product.from_dict(p).__dict__ for p in products]

    @staticmethod
    def get_product_by_name(name):
        db = current_app.mongo.db
        product = db.products.find_one({"name": name})
        return Product.from_dict(product) if product else None

    @staticmethod
    def delete_product(product_id, seller_id):
        db = current_app.mongo.db
        result = db.products.delete_one({
            "_id": ObjectId(product_id),
            "seller_id": ObjectId(seller_id)
        })
        return result.deleted_count > 0

    @staticmethod
    def update_product(product_id, seller_id, updates):
        db = current_app.mongo.db
        result = db.products.update_one(
            {"_id": ObjectId(product_id), "seller_id": ObjectId(seller_id)},
            {"$set": updates}
        )
        return result.modified_count > 0