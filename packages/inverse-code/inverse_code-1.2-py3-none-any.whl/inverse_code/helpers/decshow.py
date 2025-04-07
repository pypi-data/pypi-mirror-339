from inverse_code.ascii.win1252 import Win1252, Dec


def control_characters_0_31():
    """0 to 31"""
    result = list(Dec().code(32))
    return result


def printable_characters_32_127():
    """32 to 127"""
    result = list(Dec().code(128, 32))
    return result


def extended_ascii_128_255():
    """128 to 255"""
    result = list(Dec().code(256, 128))
    return result


def all_decimal():
    """@NOTE: Lists all decimal numbers."""
    return Win1252.dec_0_255(Win1252)
