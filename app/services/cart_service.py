from datetime import datetime

from app.models.cart_model import Cart
from app.dtos.cart_dto import CartDTO, CartItemDTO
from app.utils.exception import CartNotFound, ProductNotFound
from bson import ObjectId


class CartService:
    @staticmethod
    def create_cart(user_id=None, session_id=None, ip_address=None):
        cart = Cart.create_cart(user_id, session_id, ip_address)
        return CartService.convert_cart_to_dto(cart)

    @staticmethod
    def get_cart(cart_id):
        cart = Cart.find_cart(cart_id)
        if not cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")
        return CartService.convert_cart_to_dto(cart)

    @staticmethod
    def add_item_to_cart(cart_id, product_id, quantity, price, attributes=None):
        cart = Cart.add_item_to_cart(cart_id, product_id, quantity, price, attributes)
        if not cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")

        # Update totals
        subtotal = sum(
            item['price_at_addition'] * item['quantity']
            for item in cart['items']
        )

        updated_cart = Cart.update_cart(cart_id, {
            'subtotal': subtotal,
            'total': subtotal + cart.get('tax_amount', 0) + cart.get('shipping_amount', 0)
        })

        return CartService.convert_cart_to_dto(updated_cart)

    @staticmethod
    def remove_item_from_cart(cart_id, item_index):
        cart = Cart.find_cart(cart_id)
        if not cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")

        if item_index >= len(cart['items']):
            raise ProductNotFound(f"Item index {item_index} not found in cart")

        updated_cart = Cart.remove_item_from_cart(cart_id, item_index)
        if not updated_cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")

        # Update totals
        subtotal = sum(
            item['price_at_addition'] * item['quantity']
            for item in updated_cart['items']
        )

        updated_cart = Cart.update_cart(cart_id, {
            'subtotal': subtotal,
            'total': subtotal + updated_cart.get('tax_amount', 0) + updated_cart.get('shipping_amount', 0)
        })

        return CartService.convert_cart_to_dto(updated_cart)

    @staticmethod
    def update_item_quantity(cart_id, item_index, new_quantity):
        cart = Cart.find_cart(cart_id)
        if not cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")

        if item_index >= len(cart['items']):
            raise ProductNotFound(f"Item index {item_index} not found in cart")

        # Create update query
        update_query = {
            f'items.{item_index}.quantity': new_quantity,
            'updated_at': datetime.utcnow()
        }

        updated_cart = Cart.update_cart(cart_id, update_query)
        if not updated_cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")

        # Update totals
        subtotal = sum(
            item['price_at_addition'] * item['quantity']
            for item in updated_cart['items']
        )

        updated_cart = Cart.update_cart(cart_id, {
            'subtotal': subtotal,
            'total': subtotal + updated_cart.get('tax_amount', 0) + updated_cart.get('shipping_amount', 0)
        })

        return CartService.convert_cart_to_dto(updated_cart)

    @staticmethod
    def clear_cart(cart_id):
        updated_cart = Cart.clear_cart(cart_id)
        if not updated_cart:
            raise CartNotFound(f"Cart with ID {cart_id} not found")
        return CartService.convert_cart_to_dto(updated_cart)

    @staticmethod
    def convert_cart_to_dto(cart_doc):
        return CartDTO(
            cart_id=str(cart_doc['_id']),
            user_id=cart_doc.get('user_id'),
            status=cart_doc.get('status', 'active'),
            subtotal=cart_doc.get('subtotal', 0.0),
            tax_amount=cart_doc.get('tax_amount', 0.0),
            shipping_amount=cart_doc.get('shipping_amount', 0.0),
            total=cart_doc.get('total', 0.0),
            currency=cart_doc.get('currency', 'USD'),
            items=[
                CartItemDTO(
                    item_id=str(idx),
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    price_at_addition=item['price_at_addition'],
                    attributes=item.get('attributes', {}),
                    added_at=item['added_at']
                ) for idx, item in enumerate(cart_doc.get('items', []))
            ],
            created_at=cart_doc['created_at'],
            updated_at=cart_doc['updated_at']
        )