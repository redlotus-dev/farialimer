"module for converting datatypes to other representations"

from datetime import date

from farialimer.parser.basic_parser import ParseObject


def convert_yyyymmdd(str_date):
    """
    Given a str like 20221020
    returns a date like date(2022,10,20)
    """
    year = int(str_date[:4])
    month = int(str_date[4:6])
    day = int(str_date[6:8])

    result = date(year, month, day)
    return result


def convert_to_int(parse_obj: ParseObject):
    """given a string-like int, convert it to int"""
    return int(parse_obj.value)


def convert_to_string(parse_obj: ParseObject):
    """given a string, removes leading/trailing blank spaces"""
    return parse_obj.value.strip()


def convert_to_numeric(parse_obj: ParseObject):
    """given a parse_obj, convert to a numerico value with its decimal places"""
    return parse_obj
