from inverse_code.ascii.win1252 import Win1252, Symbol


def printable_characters_32_127():
    """32 to 127"""
    result = [x["symb"] for x in Symbol().code(128) if x["int"] > 32]
    return result


def all_symbol():
    """@NOTE: Lists all symbol."""
    return Win1252.symbol_32_127(Win1252)
