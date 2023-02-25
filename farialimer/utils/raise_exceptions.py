"""Functions that raise exceptions"""


def raise_error_for_nonascii_character(idx, line):
    """Remove non ascii characters from a line"""
    non_ascii_chars = [char for char in line if ord(char) >= 128]
    if non_ascii_chars:
        raise ValueError(
            f"Line contains non ascii characters: {non_ascii_chars} in line: {idx}"
        )
