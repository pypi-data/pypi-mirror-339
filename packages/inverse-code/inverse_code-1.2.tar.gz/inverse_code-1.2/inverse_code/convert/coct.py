from inverse_code.error import MaximumNumber, NonNumber
from inverse_code.helpers import octshow, decshow, hexshow, binshow, symbshow


def coct_decimal(char):
    """
    convert octal to decimal.\n
    @NOTE: `index_oct`: octal control Index.\n
    `result`: Records the decimal list and returns the corresponding index of the octal.\n
    returns a decimal number based on the octal index.
    """
    index_oct = 0

    try:
        if char > 377:
            raise MaximumNumber(377)

        result = decshow.all_decimal()
        for x in octshow.all_octal():
            if char == x:
                break
            index_oct += 1
        return result[index_oct]

    except TypeError as e:
        raise NonNumber from e
    except IndexError as ex:
        raise IndexError(
            f"""This ({char}) character does not correspond to the octal list.
            Please come in with a valid character."""
        ) from ex


def coct_hexadecimal(char):
    """
    convert octal to hexadecimal.\n
    """
    index_oct = 0

    try:
        if char > 377:
            raise MaximumNumber(377)

        result = hexshow.all_hexadecimal()
        for x in octshow.all_octal():
            if char == x:
                break
            index_oct += 1
        return result[index_oct]
    except TypeError as e:
        raise NonNumber from e
    except IndexError as ex:
        raise IndexError(
            f"""This ({char}) character does not correspond to the hexadecimal list.
            Please come in with a valid character."""
        ) from ex


def coct_binary(char):
    """convert octal to binary"""
    index_oct = 0

    try:
        if char > 377:
            raise MaximumNumber(377)

        result = binshow.all_binary()
        for x in octshow.all_octal():
            if char == x:
                break
            index_oct += 1
        return result[index_oct]
    except TypeError as e:
        raise NonNumber from e
    except IndexError as ex:
        raise IndexError(
            f"""This ({char}) character does not correspond to the binary list.
            Please come in with a valid character."""
        ) from ex


def coct_symbol(char):
    """
    convert octal to symbol.\n
    @NOTE: Only values is allowed from `32` to `126`.
    """
    index_oct = 0

    try:
        if char < 40:
            raise ValueError("Only values is allowed from 40 to 176.")

        if char > 176:
            raise MaximumNumber(176)

        result = symbshow.all_symbol()
        for x in octshow.all_octal():
            if char == x:
                break
            index_oct += 1
        return result[index_oct]
    except TypeError as e:
        raise NonNumber from e
    except IndexError as ex:
        raise IndexError(
            f"""This ({char}) character does not correspond to the symbol list.
            Please come in with a valid character."""
        ) from ex
