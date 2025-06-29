from app.dtos.response.ProductResponse import ProductResponse

def document_to_product_response(product_doc: dict) -> ProductResponse:
    return ProductResponse(
        id=str(product_doc["_id"]),
        name=product_doc["name"],
        description=product_doc["description"],
        price=product_doc["price"],
        category=product_doc["category"],
        stock_quantity=product_doc["stock_quantity"],
        images=product_doc["images"],
        seller_id=str(product_doc["seller_id"]),
        status=product_doc.get("status", "available"),
        created_at=product_doc["created_at"],
        updated_at=product_doc.get("updated_at")
    )
