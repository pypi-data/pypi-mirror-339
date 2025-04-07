"""
@NOTE: Formula:\n

reversing the symbol.\n
converts symbol to binary\n
- increases from 4 bits up to 32 bits.\n
- It encodes 32 bits bit to bit and returns a 4-bit binary list.\n
- the output has to be like `Reed-Solomon's error correction codes`.
converts binary to hexadecimal.\n
converts hexadecimal to decimal.\n
"""

from .convert import chex, cbin, cdec
from .error import NonNumber


def decode(decimal_number):
    """
    @NOTE: Can only be in maximum `9 characters`.\n
    `decode_raw`: increases from 4 bit up to 32 bit.\n
    """

    if len(str(decimal_number)) > 9:
        raise ValueError("Can only be in maximum 9 characters.")

    try:
        cbinary = []
        decode_raw = []
        end_of_coding = []
        chexadecimal = []
        csymbol = []

        chexadecimal = converts_decimal_hexadecimal(decimal_number)
        cbinary = converts_hexadecimal_binary(chexadecimal)
        decode_raw = increases_4_bits_up_to_32_bits(decode_raw, cbinary)
        end_of_coding = codes_bit_a_bit(end_of_coding, decode_raw)
        csymbol = converts_binary_symbol(csymbol, end_of_coding)
    except TypeError as e:
        raise NonNumber from e

    return csymbol


def converts_decimal_hexadecimal(decimal_number: int):
    """
    @NOTE: Converts `decimal` to `hexadecimal`.\n

    To convert a decimal number into hexadecimal,
    the whole decimal number is divided successively by 16 (hexadecimal system base),
    until the quotient is 0.
    The remains obtained from the divisions make up the entire part of the hexadecimal number.
    The integer hexadecimal number will be formed from the most significant digit
    (the last rest of the division) to the least significant digit
    (the first entire typot of multiplication).
    """

    start = 0
    cdecimal = []
    chexadecimal = []

    while start < 8:
        result_division = int(decimal_number / 16)  # converts to an integer.
        rest_division = decimal_number - (
            result_division * 16
        )  # returns the rest of the division.

        cdecimal.append(rest_division)
        decimal_number = result_division
        start += 1

    start = 0
    add_bit = ""
    for d in cdecimal[::-1]:  # invert the bits and convert 8bit to 4bit
        add_bit += cdec.cdec_hexadecimal(d)[1:]
        if start == 1:  # 2 bit union ["0","f","0","2"] to ["0f","02"].
            chexadecimal.append(add_bit)  # returns an 4 bit hexadecimal.
            add_bit = ""
            start = -1
        start += 1

    return chexadecimal


def converts_hexadecimal_binary(chexadecimal):
    """
    @NOTE: Converts hexadecimal to binary
    Hexadecimal numbers are converted individually by converting
    each hexadecimal digit to their binary equivalent formed by 4 or 8 bit groups.
    """

    cbinary = []

    for h in chexadecimal:
        cbinary.append(chex.chex_binary(h))
    return cbinary


def increases_4_bits_up_to_32_bits(decode_raw: list, cbinary: list):
    """
    increases from 4 bit up to 32 bit.\n

    ### running the code:

    `4bit`: ['00001111', '00000010', '00001101', '00110100']\n
    `out of the code`:\n
    `8bytes`:  [['0', '0', '0', '0', '1', '1', '1', '1'], ['0', '0', '0', '0', '0', '0', '1', '0'],
                ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '1', '1', '0', '1', '0', '0']]
    """

    start = 0
    while start < 4:
        decode_raw.append(list(cbinary[start]))  # increases from 4 bit up to 32 bit
        start += 1
    return decode_raw


def codes_bit_a_bit(end_of_coding: list, decode_raw: list):
    """
    @NOTE: It encodes 32 bits bit to bit and returns a 4-bit binary list.\n
    `decode_raw`: list of 32 bit separated by 4 bits.\n
    `start_4_bit`: 4 bit control variable [0 to 3].\n
    `bit_least_significant` and `bit_most_significant`: makes the passing of bit from [0 to 7].\n
    `encode_bit`: stores every 8 bit in the 32 bits list.\n
    `end_of_coding`: stores each 8 bit and returns a separate 4 bit list.\n

    ### running the code:

    `32bit`: [['0', '1', '0', '0', '0', '1', '0', '0'],['0', '1', '0', '0', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0', '0', '1', '0'],['0', '1', '0', '0', '0', '1', '1', '0']]\n
    `out of the code`:\n
    `4bit`: ['00001111', '00000010', '00001101', '00110100'],

    """

    start = 0
    start_4_bit = 0
    bit_least_significant = 0
    bit_most_significant = 4
    decode_8bit = ""
    start_2_bit = True

    while start < 32:
        if start_4_bit == 4:
            start_4_bit = 0

        if start_2_bit:
            # allows you to add 2 bit every 8 bit. 8bit = [abcdefgh] 2bit = [ae]
            start_2_bit = False
            decode_8bit += decode_raw[start_4_bit][bit_least_significant]
        else:
            start_2_bit = True
            decode_8bit += decode_raw[start_4_bit][bit_most_significant]
            start_4_bit += 1

        if len(decode_8bit) == 8:
            end_of_coding.append(decode_8bit)
            decode_8bit = ""
            bit_least_significant += 1
            bit_most_significant += 1
        start += 1
    return end_of_coding


def converts_binary_symbol(csymbol, end_of_coding: list):
    """
    @NOTE: Converts symbol to binary.\n
    `binary[::-1]`: reversing the binary.\n
    `csymbol`: converts binary to symbol.\n

    `out of the code`: FRED\n
    """

    character = ""
    for b in end_of_coding[::-1]:
        if b != "00000000":
            character += cbin.cbin_symbol(b)  # converts binary to symbol
    csymbol = character
    return csymbol
