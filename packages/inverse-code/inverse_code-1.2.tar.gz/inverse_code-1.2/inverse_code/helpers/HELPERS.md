# Helper

This library is responsible for listing the entire ASCII table according to your data limit. It depends on the Win1252 module of the ASCII Library.

#
modules:
1. [binshow](#binshow)
2. [decshow](#decshow)
3. [hexshow](#hexshow)
4. [octshow](#octshow)
5. [symbshow](#symbshow)
6. [helpers](#helpers)
#

1. #### binshow

### code snippets

```python
from inverse_code.ascii.win1252 import Win1252, Bin


def control_characters_0_11111():
    """0 to 1"""
    result = [x["bin"] for x in Bin().code(32)]
    return result
```

2. #### decshow

### code snippets

```python
from inverse_code.ascii.win1252 import Win1252, Dec


def printable_characters_32_127():
    """32 to 127"""
    result = list(Dec().code(128, 32))
    return result
```

3. #### hexshow

### code snippets

```python
from inverse_code.ascii.win1252 import Win1252, Hex


def extended_ascii_80_ff():
    """80 to ff"""
    result = [x["hex"] for x in Hex().code(197) if x["int"] > 80]
    return result
```

4. #### octshow

### code snippets

```python
from inverse_code.ascii.win1252 import Win1252, Oct


def extended_ascii_200_377():
    """200 to 377"""
    result = [x["oct"] for x in Oct().code(378, 200)]
    return result

```

5. #### symbshow

### code snippets

```python
from inverse_code.ascii.win1252 import Win1252, Symbol


def printable_characters_32_127():
    """32 to 127"""
    result = [x["symb"] for x in Symbol().code(95)]
    return result


def all_symbol():
    """@NOTE: Lists all symbol."""
    return Win1252.symbol_32_127(Win1252)
```

6. #### helpers

### code snippets

```python
from inverse_code.ascii.win1252 import Win1252


def all_ascii_table():
    """@NOTE: Lists all ascii table"""
    decshow = Win1252.dec_0_255(Win1252)
    octshow = Win1252.oct_000_377(Win1252)
    hexshow = Win1252.hex_00_ff(Win1252)
    binshow = Win1252.bin_01(Win1252)
    symbolhow = Win1252.symbol_32_127(Win1252)

    result = {
        "decimal": decshow,
        "octal": octshow,
        "hexadecimal": hexshow,
        "binary": binshow,
        "symbol": symbolhow,
    }
    return result
```
