from inverse_code.helpers import hexshow, decshow, octshow, binshow, symbshow


def cbin_octal(char):
    """convert binary to octal"""
    index_hex = 0

    try:
        result = octshow.all_octal()
        for x in binshow.all_binary():
            if char == x:
                break
            index_hex += 1
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the binary list.
           Please enter with a valuable value."""
        ) from e


def cbin_decimal(char):
    """convert binary to decimal"""
    index_hex = 0

    try:
        result = decshow.all_decimal()
        for x in binshow.all_binary():
            if char == x:
                break
            index_hex += 1
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the binary list.
           Please enter with a valuable value."""
        ) from e


def cbin_hexadecimal(char):
    """convert binary to hexadecimal"""
    index_hex = 0

    try:
        result = hexshow.all_hexadecimal()
        for x in binshow.all_binary():
            if char == x:
                break
            index_hex += 1
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the binary list.
           Please enter with a valuable value."""
        ) from e


def cbin_symbol(char):
    """
    convert binary to symbol.\n
    @NOTE: Only values is allowed from `20` to `7f`.
    """
    index_hex = 0

    try:

        result = symbshow.all_symbol()
        for x in binshow.all_binary():
            if char == x:
                break
            index_hex += 1
        if index_hex < 32:
            raise ValueError(
                "The allowed list is only: ASCII printable characters (character code 32-127)"
            )
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the ASCII printable characters 
            (character code 00100000-01111111).
            Please enter with a valuable value."""
        ) from e
