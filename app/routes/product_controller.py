from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.dtos.request.product_request import CreateProductRequest
from app.models.product_model import Product
from app.services.productService import ProductService

product_bp = Blueprint('product_bp', __name__, url_prefix='/api/products')

@product_bp.route('/create', methods=['POST'])
def create_product():
    try:
        body = request.get_json()
        product_data = CreateProductRequest(**body)
        if not product_data.images or len(product_data.images) == 0:
            return jsonify({"error": "At least one image is required."}), 400
        product_id = ProductService.create_product(product_data)
        return jsonify({"message":"product created successfully", "product_id": product_id}), 201
    except ValidationError as error:
        return jsonify({"error":"validation error", "details":error.errors()}), 422
    except ValueError as error:
        return jsonify({"error":str(error)}), 409
    except Exception as error:
        return jsonify({"error":"Unexpected error", "details":str(error)}), 500

@product_bp.route('/update', methods=['GET'])
def get_all_products():
    try:
        products = ProductService.get_all_products()
        return jsonify(products), 200
    except Exception as error:
        return jsonify({"error":"Failed to fetch products", "details":str(error)}), 404

@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return jsonify({"error":"Product not found"}), 404
        return jsonify(product), 200
    except Exception as error:
        return jsonify({"error":"Failed to fetch product", "details":str(error)}), 500

@product_bp.route('/search', methods=['GET'])
def get_product_by_name():
    name=request.args.get("name")
    if not name:
        return jsonify({"error":"product name is required"}), 400
    try:
        products = ProductService.get_product_by_name(name)
        if not products:
            return jsonify({"error":"Product not found"}), 404
        return jsonify(products), 200
    except Exception as error:
        return jsonify({"error":"Failed to fetch products by name", "details":str(error)}), 500

@product_bp.route('/<product_id>', methods=['DELETE'])

def delete_product(product_id):
    data = request.get_json()
    seller_id = data.get('seller_id')

    if not seller_id:
        return jsonify({"error":"seller ID is required"}), 400
    try:
        deleted = ProductService.delete_product(product_id, seller_id)
        if not deleted:
            return jsonify({"error":"Product not found or was not uploaded"}), 404
        return jsonify({"message":"product deleted successfully"}), 200
    except Exception as error:
        return jsonify({"error":"Failed to fetch product", "details":str(error)}), 500

@product_bp.route('/<product_id>/update', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        seller_id = data.get('seller_id')
        if not seller_id:
            return jsonify({"error":"seller ID is required"}), 400
        update_fields = data.get('update_fields')
        if not update_fields:
            return jsonify({"error":"update_fields is required"}), 400
        successful = ProductService.update_product(product_id, seller_id, update_fields)
        if successful:
            return jsonify({"message":"product updated successfully"}), 200
        else:
            return jsonify({"error":"Product not found or not own by the seller "}), 404
    except Exception as error:
        return jsonify({"error":"Failed to fetch product", "details":str(error)}), 500

