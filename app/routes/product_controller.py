from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.dtos.request.product_request import CreateProductRequest
from app.dtos.response.ProductResponse import ProductResponse
from app.services.productService import ProductService

product_bp = Blueprint("product_bp", __name__, url_prefix="/api/products")

@product_bp.route("/create", methods=["POST"])
def create_product():
    try:
        data = request.get_json()
        product_data = CreateProductRequest(**data)

        if not product_data.images or len(product_data.images) == 0:
            return jsonify({"error": "At least one image is required."}), 400


        product_id = ProductService.create_product(product_data)
        return jsonify({"message": "Product created successfully", "product_id": product_id}), 201

    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 422
    except Exception as e:
        import traceback
        print("ERROR:", traceback.format_exc())
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

@product_bp.route("/", methods=["GET"])
def get_all_products():
    try:
        products = ProductService.get_all_products()
        response = [ProductResponse.from_model(p).model_dump(mode="json") for p in products]
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch products", "details": str(e)}), 500


@product_bp.route("/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        response = ProductResponse.from_model(product).model_dump(mode="json")
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch product", "details": str(e)}), 500


@product_bp.route("/search", methods=["GET"])
def get_product_by_name():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Product name is required"}), 400
    try:
        product = ProductService.get_product_by_name(name)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        response = ProductResponse.from_model(product)
        return jsonify(response.model_dump(mode="json")), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch product by name", "details": str(e)}), 500


@product_bp.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        data = request.get_json()
        seller_id = data.get("seller_id")

        if not seller_id:
            return jsonify({"error": "Seller ID is required"}), 400

        deleted = ProductService.delete_product(product_id, seller_id)
        if not deleted:
            return jsonify({"error": "Product not found or unauthorized"}), 404

        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete product", "details": str(e)}), 500


@product_bp.route("/<product_id>/update", methods=["PUT"])
def update_product(product_id):
    try:
        data = request.get_json()
        seller_id = data.get("seller_id")
        update_fields = data.get("update_fields")

        if not seller_id:
            return jsonify({"error": "Seller ID is required"}), 400
        if not update_fields:
            return jsonify({"error": "update_fields is required"}), 400

        updated = ProductService.update_product(product_id, seller_id, update_fields)
        if not updated:
            return jsonify({"error": "Product not found or unauthorized"}), 404

        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update product", "details": str(e)}), 500
