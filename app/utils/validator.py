from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException


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