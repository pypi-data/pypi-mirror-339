from inverse_code.ascii.win1252 import Win1252, Bin


def control_characters_0_11111():
    """0 to 1"""
    result = [x["bin"] for x in Bin().code(32)]
    return result


def printable_characters_100000_01111111():
    """0 to 1"""
    list_bin = list(Bin().code(128))
    result = [x["bin"] for x in list_bin if x["int"] > 32]
    return result


def extended_ascii_10000000_11111111():
    """0 to 1"""
    result = [x["bin"] for x in Bin().code(256) if x["int"] > 128]
    return result


def all_binary():
    """@NOTE: Lists all binary numbers."""
    return Win1252.bin_01(Win1252)
