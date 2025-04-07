# Convert

This sub library is responsible for converting `binary, decimal, octal, hexadecimal and symbols`.
It inherits the functions of the `library of helpers` to do the conversions.

#### Summary
#
modules:
1. [cbin](#cbin)
2. [cdec](#cdec)
3. [chex](#chex)
4. [coct](#coct)
5. [csymb](#csymb)

#

1. #### cbin

- def cbin_octal(char): convert binary to octal
- def cbin_decimal(char): convert binary to decimal
- def cbin_hexadecimal(char): convert binary to hexadecimal
- def cbin_symbol(char): convert binary to symbol.\n

### code snippets

```python
from inverse_code.helpers import octshow, binshow

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

```

2. #### cdec

- def cdec_octal(char): convert decimal to octal
- def cdec_hexadecimal(char): convert decimal to hexadecimal
- def cdec_binary(char): convert decimal to binary
- def cdec_symbol(char): convert decimal to symbol.

### code snippets

```python
from inverse_code.error import MaximumNumber, NonNumber
from inverse_code.helpers import hexshow

def cdec_hexadecimal(char):
    """convert decimal to hexadecimal"""

    try:
        if char > 255:
            raise MaximumNumber(255)

        result = hexshow.all_hexadecimal()
        return result[char]
    except TypeError as e:
        raise NonNumber from e

```

3. #### chex

- def chex_octal(char): convert hexadecimal to octal
- def chex_decimal(char: str): convert hexadecimal to decimal
- def chex_binary(char): convert hexadecimal to binary
- def chex_symbol(char): convert hexadecimal to symbol.

### code snippets

```python
from inverse_code.helpers import hexshow, binshow

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

```

4. #### coct

- def coct_decimal(char):convert octal to decimal.
- def coct_hexadecimal(char): convert octal to hexadecimal.
- def coct_binary(char): convert octal to binary
- def coct_symbol(char): convert octal to symbol.

### code snippets

```python
from inverse_code.error import MaximumNumber, NonNumber
from inverse_code.helpers import octshow, binshow

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

```

5. #### csymb

- def csymb_octal(char): convert symbol to octal
- def csymb_decimal(char): convert symbol to decimal
- def csymb_hexadecimal(char): convert symbol to hexadecimal
- def csymb_binary(char): convert binary to symbol.
- def validate(index_hex): return raise

```python
from inverse_code.helpers import hexshow, symbshow

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


def validate(index_hex):
    """return raise"""
    if index_hex < 32 or index_hex > 127:
        raise ValueError("The allowed list is only: ASCII printable characters.")


```