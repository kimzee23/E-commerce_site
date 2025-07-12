from datetime import datetime
from bson import ObjectId
from app.extentions import mongo
from pymongo import ReturnDocument


class Cart:
    @staticmethod
    def create_cart(user_id=None, session_id=None, ip_address=None):
        cart_data = {
            'user_id': user_id,
            'session_id': session_id,
            'status': 'active',
            'subtotal': 0.0,
            'tax_amount': 0.0,
            'shipping_amount': 0.0,
            'total': 0.0,
            'currency': 'USD',
            'ip_address': ip_address,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'items': []
        }
        result = mongo.db.carts.insert_one(cart_data)
        return mongo.db.carts.find_one({'_id': result.inserted_id})

    @staticmethod
    def find_cart(cart_id):
        if not ObjectId.is_valid(cart_id):
            return None
        return mongo.db.carts.find_one({'_id': ObjectId(cart_id)})

    @staticmethod
    def update_cart(cart_id, update_data):
        if not ObjectId.is_valid(cart_id):
            return None
        return mongo.db.carts.find_one_and_update(
            {'_id': ObjectId(cart_id)},
            {'$set': update_data},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    def add_item_to_cart(cart_id, product_id, quantity, price, attributes=None):
        if not ObjectId.is_valid(cart_id):
            return None

        new_item = {
            'product_id': product_id,
            'quantity': quantity,
            'price_at_addition': price,
            'attributes': attributes or {},
            'added_at': datetime.utcnow()
        }

        return mongo.db.carts.find_one_and_update(
            {'_id': ObjectId(cart_id)},
            {
                '$push': {'items': new_item},
                '$set': {'updated_at': datetime.utcnow()}
            },
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    def remove_item_from_cart(cart_id, item_index):
        if not ObjectId.is_valid(cart_id):
            return None

        return mongo.db.carts.find_one_and_update(
            {'_id': ObjectId(cart_id)},
            {
                '$unset': {f'items.{item_index}': 1},
                '$pull': {'items': None},
                '$set': {'updated_at': datetime.utcnow()}
            },
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    def clear_cart(cart_id):
        if not ObjectId.is_valid(cart_id):
            return None

        return mongo.db.carts.find_one_and_update(
            {'_id': ObjectId(cart_id)},
            {
                '$set': {
                    'items': [],
                    'subtotal': 0.0,
                    'tax_amount': 0.0,
                    'shipping_amount': 0.0,
                    'total': 0.0,
                    'updated_at': datetime.utcnow()
                }
            },
            return_document=ReturnDocument.AFTER
        )