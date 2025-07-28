import re


def format_phone_number(raw: str) -> str:
    digits = re.sub(r"\D", "", raw)

    if len(digits) == 9:
        digits = "0" + digits

    if len(digits) == 10 and digits.startswith("09"):
        return f"0{digits[1:4]}-{digits[4:7]}-{digits[7:]}"

    return raw
