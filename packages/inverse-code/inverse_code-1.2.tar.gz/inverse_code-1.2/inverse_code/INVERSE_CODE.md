# Inverse code

It is the main library that incorporates the ascii, convert, helpers libraries and the coding, decoding and error modules.

## modules
- [encode](#encode)
- [decode](#decode)
- [error](#error)

#

- #### encode

Reversing the symbol. Converts symbol to binary. Increases from 4 bits up to 32 bits. It encodes 32 bits bit to bit and returns a 4-bit binary list. The output has to be like `Reed-Solomon's error correction codes`. Converts binary to hexadecimal. Converts hexadecimal to decimal.

### code snippets

```python
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

```

- #### decode

Reversing the symbol. Converts symbol to binary
increases from 4 bits up to 32 bits. It encodes 32 bits bit to bit and returns a 4-bit binary list. The output has to be like `Reed-Solomon's error correction codes`. Converts binary to hexadecimal. Converts hexadecimal to decimal.

### code snippets

```python
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
```

- #### error
```python
"""This method returns personalized error message."""

class NonNumber(TypeError):
    """@NOTE: Expect a TypeError for non-numeric inputs."""

    def __init__(self):
        super().__init__("Only Integer numbers is allowed.")


class NonNegativeNumber(ValueError):
    """@NOTE: Permitted values are higher than 0."""

    def __init__(self):
        super().__init__("Permitted values are higher than 0.")


class MaximumNumber(ValueError):
    """@NOTE: The maximum number of a list."""

    def __init__(self, max_number):
        super().__init__(f"The maximum number of this list is {max_number}.")
```