from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
from bson import ObjectId
from app.utils.exception import InvalidObjectId, InvalidQuantity, InvalidPrice


def validation_for_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

SUPPORTED_REGIONS = ["US", "GB", "NG", "IN", "CN", "JP", "KR", "SG", "MY", "PH", "ID", "PK"]

def validation_for_phoneNumber(phone_number):
    for region in SUPPORTED_REGIONS:
        try:
            parsed_number = phonenumbers.parse(phone_number, region)
            if phonenumbers.is_valid_number(parsed_number):
                return True
        except NumberParseException:
            continue
    return False



def validate_object_id(object_id):
    """Validate MongoDB ObjectId"""
    if not ObjectId.is_valid(object_id):
        raise InvalidObjectId(object_id)


def validate_quantity(quantity):
    """Validate product quantity"""
    if not isinstance(quantity, int) or quantity <= 0:
        raise InvalidQuantity()


def validate_price(price):
    """Validate product price"""
    if not isinstance(price, (int, float)) or price <= 0:
        raise InvalidPrice()


def validate_cart_data(data):
    """Validate cart creation/update data"""
    required_fields = ['user_id', 'session_id']
    if not any(field in data for field in required_fields):
        raise ValueError("Either user_id or session_id must be provided")


def validate_cart_item_data(data):
    """Validate cart item data"""
    required_fields = ['product_id', 'price']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    validate_price(data['price'])
    if 'quantity' in data:
        validate_quantity(data['quantity'])