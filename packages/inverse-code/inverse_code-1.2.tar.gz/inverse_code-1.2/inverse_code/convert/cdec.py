from inverse_code.error import MaximumNumber, NonNumber
from inverse_code.helpers import octshow, hexshow, binshow, symbshow


def cdec_octal(char):
    """convert decimal to octal"""

    try:
        if char > 255:
            raise MaximumNumber(255)

        result = octshow.all_octal()
        return result[char]
    except TypeError as e:
        raise NonNumber from e


def cdec_hexadecimal(char):
    """convert decimal to hexadecimal"""

    try:
        if char > 255:
            raise MaximumNumber(255)

        result = hexshow.all_hexadecimal()
        return result[char]
    except TypeError as e:
        raise NonNumber from e


def cdec_binary(char):
    """convert decimal to binary"""

    try:
        if char > 255:
            raise MaximumNumber(255)

        result = binshow.all_binary()
        return result[char]
    except TypeError as e:
        raise NonNumber from e


def cdec_symbol(char):
    """
    convert decimal to symbol.\n
    @NOTE: Only values is allowed from `32` to `126`.
    """

    try:
        if char > 126:
            raise MaximumNumber(126)

        if char < 32:
            raise ValueError("Only values is allowed from 32 to 126.")

        result = symbshow.all_symbol()
        return result[char]
    except TypeError as e:
        raise NonNumber from e
