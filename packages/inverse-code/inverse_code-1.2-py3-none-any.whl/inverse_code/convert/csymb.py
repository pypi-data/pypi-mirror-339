from inverse_code.helpers import hexshow, decshow, octshow, binshow, symbshow


def csymb_octal(char):
    """convert symbol to octal"""
    index_hex = 0

    try:
        result = octshow.all_octal()
        for x in symbshow.all_symbol():
            if char == x:
                break
            index_hex += 1
        validate(index_hex)
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the symbol list.
           Please enter with a valuable value."""
        ) from e


def csymb_decimal(char):
    """convert symbol to decimal"""
    index_hex = 0

    try:
        result = decshow.all_decimal()
        for x in symbshow.all_symbol():
            if char == x:
                break
            index_hex += 1
        validate(index_hex)
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the symbol list.
           Please enter with a valuable value."""
        ) from e


def csymb_hexadecimal(char):
    """convert symbol to hexadecimal"""
    index_hex = 0

    try:
        result = hexshow.all_hexadecimal()
        for x in symbshow.all_symbol():
            if char == x:
                break
            index_hex += 1
        validate(index_hex)
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the symbol list.
           Please enter with a valuable value."""
        ) from e


def csymb_binary(char):
    """
    convert binary to symbol.\n
    @NOTE: Only values is allowed from `20` to `7f`.
    """
    index_hex = 0

    try:
        result = binshow.all_binary()
        for x in symbshow.all_symbol():
            if char == x:
                break
            index_hex += 1
        validate(index_hex)
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the ASCII printable characters 
            (character code 00100000-01111111).
            Please enter with a valuable value."""
        ) from e


def validate(index_hex):
    """return raise"""
    if index_hex < 32 or index_hex > 127:
        raise ValueError("The allowed list is only: ASCII printable characters.")
