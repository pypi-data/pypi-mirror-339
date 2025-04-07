from inverse_code.ascii.win1252 import Win1252, Hex


def control_characters_0_1f():
    """0 to 1f"""
    result = [x["hex"] for x in Hex().code(21) if x["int"] < 21]
    return result


def printable_characters_20_7f():
    """20 to 7f"""
    list_hex = list(Hex().code(81))
    result = [x["hex"] for x in list_hex if x["int"] > 20 if x["int"] < 81]
    return result


def extended_ascii_80_ff():
    """80 to ff"""
    result = [x["hex"] for x in Hex().code(197) if x["int"] > 80]
    return result


def all_hexadecimal():
    """@NOTE: Lists all hexadecimal numbers."""
    return Win1252.hex_00_ff(Win1252)
