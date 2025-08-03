from flask import Blueprint, request, jsonify
from app.services.cart_service import CartService
# from app.utils.exception import CartNotFound, ProductNotFound
from app.utils.validator import validate_object_id

cart_bp = Blueprint('cart', __name__, url_prefix='/api/carts')


@cart_bp.route('/', methods=['POST'])
def create_cart():
    data = request.json
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    ip_address = request.remote_addr

    cart_dto = CartService.create_cart(user_id, session_id, ip_address)
    return jsonify(cart_dto.__dict__), 201


@cart_bp.route('/<string:cart_id>', methods=['GET'])
def get_cart(cart_id):
    validate_object_id(cart_id)
    cart_dto = CartService.get_cart(cart_id)
    return jsonify(cart_dto.__dict__)


@cart_bp.route('/<string:cart_id>/items', methods=['POST'])
def add_item(cart_id):
    validate_object_id(cart_id)
    data = request.json
    cart_dto = CartService.add_item_to_cart(
        cart_id=cart_id,
        product_id=data['product_id'],
        quantity=data.get('quantity', 1),
        price=data['price'],
        attributes=data.get('attributes')
    )
    return jsonify(cart_dto.__dict__)


@cart_bp.route('/<string:cart_id>/items/<int:item_index>', methods=['DELETE'])
def remove_item(cart_id, item_index):
    validate_object_id(cart_id)
    cart_dto = CartService.remove_item_from_cart(cart_id, item_index)
    return jsonify(cart_dto.__dict__)


@cart_bp.route('/<string:cart_id>/items/<int:item_index>', methods=['PUT'])
def update_item(cart_id, item_index):
    validate_object_id(cart_id)
    data = request.json
    cart_dto = CartService.update_item_quantity(
        cart_id=cart_id,
        item_index=item_index,
        new_quantity=data['quantity']
    )
    return jsonify(cart_dto.__dict__)


@cart_bp.route('/<string:cart_id>/clear', methods=['POST'])
def clear_cart(cart_id):
    validate_object_id(cart_id)
    cart_dto = CartService.clear_cart(cart_id)
    return jsonify(cart_dto.__dict__)