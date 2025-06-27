from email_validator import validate_email, EmailNotValidError
import phonenumbers


def validation_for_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validation_for_phoneNumber(phone):
    try:
         numbers = phonenumbers.parse(phone, "NG")
         return phonenumbers.is_valid_number(numbers)
    except phonenumbers.NumberParseException:
         return False