import re

def format_phone(phone: str) -> str:
    return re.sub(r"^0?(\d{2})" , r"55\1", phone)

def format_address(address_row: str) -> str:

    return re.sub(r", Rio.*", '', address_row)

