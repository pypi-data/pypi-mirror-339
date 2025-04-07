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

from .convert import csymb, chex, cbin, cdec


def encode(characters):
    """
    @NOTE: Can only be in maximum `4 characters`.\n
    `decode_raw`: increases from 4 bit up to 32 bit.\n
    """

    if len(characters) > 4:
        raise ValueError("Can only be in maximum 4 characters.")

    cbinary = []
    decode_raw = []
    end_of_coding = []
    chexadecimal = []
    cdecimal = []

    characters = single_character(characters)
    cbinary = converts_symbol_to_binary(characters, cbinary)
    decode_raw = increases_4_bits_up_to_32_bits(decode_raw, cbinary)
    end_of_coding = encodes_bit_a_bit(end_of_coding, decode_raw)
    chexadecimal = converts_binary_to_hexadecimal(chexadecimal, end_of_coding)
    cdecimal = converts_hexadecimal_to_decimal(chexadecimal)

    return cdecimal


def single_character(characters: str):
    """
    when encoding a chunk with fewer than four characters, the input should be zero-padded to
    a length of four before encoding.\n

    ### running the code:

    ```python
    characters = "A"

    while len(characters) < 4:
        characters += "0"
    ```
    `out of the code`: A000\n
    """
    while len(characters) < 4:
        characters += "0"
    return characters


def converts_symbol_to_binary(characters: str, cbinary: list):
    """
    @NOTE: Converts symbol to binary.\n
    `characters[::-1]`: reversing the characters.\n
    `cbinary`: converts characters to binary.\n
    \n
    ### running the code:

    ```python
    characters = "FRED"

    for b in characters[::-1]:
        if b == "0":
            cbinary.append(cdec.cdec_binary(0))  # converts decimal [0] to binary
        else:
            cbinary.append(csymb.csymb_binary(b)) # converts symbol to binary
    ```
    `out of the code`: DERF\n
    """
    for b in characters[::-1]:
        if b == "0":
            cbinary.append(cdec.cdec_binary(0))  # converts decimal [0] to binary
        else:
            cbinary.append(csymb.csymb_binary(b))  # converts symbol to binary
    return cbinary


def increases_4_bits_up_to_32_bits(decode_raw: list, cbinary: list):
    """
    increases from 4 bit up to 32 bit.\n

    ### running the code:

    `4bit`: ['01000100', '01000101', '01010010', '01000110']\n
    `out of the code`:\n
    `8bytes`: [['0', '1', '0', '0', '0', '1', '0', '0'],['0', '1', '0', '0', '0', '1', '0', '1'],
            ['0', '1', '0', '1', '0', '0', '1', '0'],['0', '1', '0', '0', '0', '1', '1', '0']]
    """

    start = 0
    while start < 4:
        decode_raw.append(list(cbinary[start]))  # increases from 4 bit up to 32 bit
        start += 1
    return decode_raw


def encodes_bit_a_bit(end_of_coding: list, decode_raw: list):
    """
    @NOTE: It encodes 32 bits bit to bit and returns a 4-bit binary list.\n
    `decode_raw`: list of 32 bit separated by 4 bits.\n
    `start_4_bit`: 4 bit control variable [0 to 3].\n
    `index`: makes the passing of bit from [0 to 7].\n
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
    index_x = 0
    encode_bit = ""

    while start < 32:
        if start_4_bit == 4:
            start_4_bit = 0
            index_x += 1

        encode_bit += decode_raw[start_4_bit][index_x]
        if len(encode_bit) == 8:
            end_of_coding.append(encode_bit)
            encode_bit = ""
        start_4_bit += 1
        start += 1
    return end_of_coding


def converts_binary_to_hexadecimal(chexadecimal: list, end_of_coding: list):
    """converts binary to hexadecimal"""

    for h in end_of_coding:
        chexadecimal.append(cbin.cbin_hexadecimal(h))
    return chexadecimal


def converts_hexadecimal_to_decimal(chexadecimal: list):
    """
    @NOTE: Converts hexadecimal to decimal.\n
    Formula:\n
    (hex)16=(x)10
    """

    base = 0
    b = []
    add_8bit = []

    for d in chexadecimal:
        count = 0
        while count < 2:
            if count == 0:
                add_8bit.append(d[:1])  # add only the first digito
            else:
                add_8bit.append(d[1:])  # add only the last digito
            count += 1

    for c in add_8bit:
        b.append(
            chex.chex_decimal("0" + c)  # "0": is to complement hexadecimal bit
        )  # converts the 8bit from hexadecimal to decimal

    base = (
        (b[0] * 16**7)
        + (b[1] * 16**6)
        + (b[2] * 16**5)
        + (b[3] * 16**4)
        + (b[4] * 16**3)
        + (b[5] * 16**2)
        + (b[6] * 16**1)
        + (b[7] * 16**0)
    )  # formula to calculate the hexadecimal

    return base
