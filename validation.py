import phonenumbers
import re

def phone_number_is_valid(phone_number: str) -> bool:
    try:
        phone_number_parsed = phonenumbers.parse(phone_number)
        return phonenumbers.is_possible_number(phone_number_parsed) and phonenumbers.is_valid_number(phone_number_parsed)
    except phonenumbers.NumberParseException:
        return False
    
def email_is_valid(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None