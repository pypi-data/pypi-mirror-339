from inverse_code.ascii.win1252 import Win1252, Oct


def control_characters_0_37():
    """0 to 37"""
    result = [x["oct"] for x in Oct().code(38)]
    return result


def printable_characters_40_177():
    """40 to 177"""
    result = [x["oct"] for x in Oct().code(178, 40)]
    return result


def extended_ascii_200_377():
    """200 to 377"""
    result = [x["oct"] for x in Oct().code(378, 200)]
    return result


def all_octal():
    """@NOTE: Lists all octal numbers."""
    return Win1252.oct_000_377(Win1252)
