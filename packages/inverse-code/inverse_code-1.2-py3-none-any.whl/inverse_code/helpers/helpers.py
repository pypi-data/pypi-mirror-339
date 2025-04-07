from inverse_code.ascii.win1252 import Win1252


def all_ascii_table():
    """@NOTE: Lists all ascii table"""
    decshow = Win1252.dec_0_255(Win1252)
    octshow = Win1252.oct_000_377(Win1252)
    hexshow = Win1252.hex_00_ff(Win1252)
    binshow = Win1252.bin_01(Win1252)
    symbolhow = Win1252.symbol_32_127(Win1252)

    result = {
        "decimal": decshow,
        "octal": octshow,
        "hexadecimal": hexshow,
        "binary": binshow,
        "symbol": symbolhow,
    }
    return result
