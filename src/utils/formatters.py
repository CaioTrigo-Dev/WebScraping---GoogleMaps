import re

def format_phone(phone: str) -> str:
    return re.sub(r"^0?(\d{2})" , r"55\1", phone)

def format_andress(andress_row: str) -> str:

    return re.sub(r", Rio.*", '', andress_row)

