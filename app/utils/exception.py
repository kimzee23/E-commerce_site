class APIException(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

class CartNotFound(APIException):
    """Raised when a cart is not found"""
    def __init__(self, message):
        super().__init__(message, status_code=404)

class ProductNotFound(APIException):
    """Raised when a product is not found"""
    def __init__(self, message):
        super().__init__(message, status_code=404)

class InvalidQuantity(APIException):
    """Raised when an invalid quantity is provided"""
    def __init__(self, message="Quantity must be a positive integer"):
        super().__init__(message, status_code=400)

class InvalidPrice(APIException):
    """Raised when an invalid price is provided"""
    def __init__(self, message="Price must be a positive number"):
        super().__init__(message, status_code=400)

class InvalidObjectId(APIException):
    """Raised when an invalid MongoDB ObjectId is provided"""
    def __init__(self, invalid_id):
        super().__init__(f"Invalid ID format: {invalid_id}", status_code=400)

class DatabaseError(APIException):
    """Raised when there's a database operation error"""
    def __init__(self, message="Database operation failed"):
        super().__init__(message, status_code=500)