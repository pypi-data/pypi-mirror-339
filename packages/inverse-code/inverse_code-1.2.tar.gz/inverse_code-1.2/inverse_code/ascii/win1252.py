from .asciitable import Dec, Oct, Hex, Bin, Symbol


class Win1252:
    """
    ASCII, stands for American Standard Code for Information Interchange.
    This class shows the extended ASCII table which is based on the Windows-1252
    character set which is an 8 bit ASCII table with 256 characters and symbols.
    It includes all ASCII codes from standard ASCII,
    and it is a superset of ISO 8859-1 in terms of printable characters.
    In the range 128 to 159 (hex 80 to 9F), ISO/IEC 8859-1 has invisible control characters,
    while Windows-1252 has writable characters.
    Windows-1252 is probably the most-used 8-bit character encoding in the world.
    """

    def __init__(self): ...

    def dec_0_255(self):
        """return a list of 0 to 255"""
        result = list(Dec().code(256))
        return result

    def oct_000_377(self):
        """return a list of 0 to 377 octal"""
        result = [x["oct"] for x in Oct().code(378)]
        return result

    def hex_00_ff(self):
        """return a list of 0 to ff hexadecimal"""
        result = [x["hex"] for x in Hex().code(197)]
        return result

    def bin_01(self):
        """return a list of 00000000 to 11111111 binary numbers"""
        result = [x["bin"] for x in Bin().code(256)]
        return result

    def symbol_32_127(self):
        """return a list of 32 to 127 symbol"""
        result = [x["symb"] for x in Symbol().code(128)]
        return result
