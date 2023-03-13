"module for converting datatypes to other representations"

import re
from datetime import date
from decimal import Decimal

from farialimer.parser.models import ParseObject


def convert_yyyymmdd(parse_obj: ParseObject):
    """
    Given a str like 20221020
    returns a date like date(2022,10,20)
    """
    if not parse_obj.value or parse_obj.value == "".zfill(8):
        return None
    year = int(parse_obj.value[:4])
    month = int(parse_obj.value[4:6])
    day = int(parse_obj.value[6:8])

    result = date(year, month, day)
    return result


def convert_yyyy_mm_dd(parse_obj: ParseObject):
    """
    Given a str like 2022-10-20
    returns a date like date(2022,10,20)
    """
    if not parse_obj.value or parse_obj.value.isspace():
        return None
    year, month, day = parse_obj.value.split("-")
    result = date(int(year), int(month), int(day))
    return result


def convert_to_int(parse_obj: ParseObject):
    """given a string-like int, convert it to int"""
    if not parse_obj.value or parse_obj.value.isspace():
        return None
    return int(parse_obj.value)


def convert_to_string(parse_obj: ParseObject):
    """given a string, removes leading/trailing blank spaces"""
    return parse_obj.value.strip()


def b3_convert_to_numeric(parse_obj: ParseObject):
    """given a parse_obj, convert to a numerico value with its decimal places"""
    if not parse_obj.value or parse_obj.value.isspace():
        return None
    str_int_len, str_dec_len = re.search(
        r"N\((\d+)\)V(\d+)", parse_obj.datatype
    ).groups()
    int_len = int(str_int_len)
    dec_len = int(str_dec_len)

    value = parse_obj.value.zfill(int_len + dec_len)

    integer_part = str(int(value[:int_len]))
    decimal_part = str(int(value[-dec_len:]))
    numeric_value_str = ".".join([integer_part, decimal_part])
    numeric_value = Decimal(numeric_value_str)
    return numeric_value


def febraban_convert_to_numeric(parse_obj: ParseObject):
    """given a parse_obj, convert to a numerico value with its decimal places"""
    if not parse_obj.value or parse_obj.value.isspace():
        return None
    str_int_len, str_dec_len = re.search(
        r"9\((\d+)\)V(\d+)", parse_obj.datatype
    ).groups()
    int_len = int(str_int_len)
    dec_len = int(str_dec_len)

    value = parse_obj.value.zfill(int_len + dec_len)

    integer_part = str(int(value[:int_len]))
    decimal_part = str(int(value[-dec_len:]))
    numeric_value_str = ".".join([integer_part, decimal_part])
    numeric_value = Decimal(numeric_value_str)
    return numeric_value
