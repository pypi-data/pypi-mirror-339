from inverse_code.helpers import hexshow, decshow, octshow, binshow, symbshow


def chex_octal(char):
    """convert hexadecimal to octal"""
    index_hex = 0

    try:
        result = octshow.all_octal()
        for x in hexshow.all_hexadecimal():
            if char == x:
                break
            index_hex += 1
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the hexadecimal list.
           Please enter with a valuable value."""
        ) from e


def chex_decimal(char: str):
    """convert hexadecimal to decimal"""
    index_hex = 0

    try:
        result = decshow.all_decimal()
        for x in hexshow.all_hexadecimal():
            if char == x:
                break
            index_hex += 1
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the hexadecimal list.
           Please enter with a valuable value."""
        ) from e


def chex_binary(char):
    """convert hexadecimal to binary"""
    index_hex = 0

    try:
        result = binshow.all_binary()
        for x in hexshow.all_hexadecimal():
            if char == x:
                break
            index_hex += 1
        return result[index_hex]
    except IndexError as e:
        raise IndexError(
            f"""This ({char}) character does not correspond to the hexadecimal list.
           Please enter with a valuable value."""
        ) from e


def chex_symbol(char):
    """
    convert hexadecimal to symbol.\n
    @NOTE: Only values is allowed from `20` to `7f`.
    """
    index_hex = 0

    try:

        result = symbshow.all_symbol()
        for x in hexshow.all_hexadecimal():
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
            f"""This ({char}) character does not correspond to the hexadecimal list.
           Please enter with a valuable value."""
        ) from e
