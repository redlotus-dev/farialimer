"module for converting datatypes to other representations"

from datetime import date


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
