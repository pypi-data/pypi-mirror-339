# ASCII


[ASCII](https://www.ascii-code.com/), stands for American Standard Code for Information Interchange. It is a 7-bit character code where each individual bit represents a unique character. This page shows the extended ASCII table which is based on the Windows-1252 character set which is an 8 bit ASCII table with 256 characters and symbols. It includes all ASCII codes from standard ASCII, and it is a superset of ISO 8859-1 in terms of printable characters. In the range 128 to 159 (hex 80 to 9F), ISO/IEC 8859-1 has invisible control characters, while Windows-1252 has writable characters. Windows-1252 is probably the most-used 8-bit character encoding in the world.

### Modules
- [asciitable](#asciitable)
- [win1252](#win1252)

### asciitable
This is where all logic of the creation of the ASCII table, divided class `decimal, hexadecimal, binary, symbol or character` and has a validation function.

#### The return of each class is an iterator (yield).
1. decimal: returns an integer
2. octal: returns an dict {"int": start, "oct": new_start}
3. hexadecimal: returns an dict {"int": self.__start, "hex": self.__result}
4. binary: returns an dict {"int": self.__start, "bin": result}
2. symbol: returns an dict {"int": self.__start, "symb": result}
2. def validate: raise an exception

### win1252
Here is all the control functions inherited from the asciitable method.

1. def dec_0_255(self): return a list of 0 to 255
2. def oct_000_377(self): return a list of 0 to 377 octal
3. def hex_00_ff(self): return a list of 0 to ff hexadecimal
4. def bin_01(self): return a list of 00000000 to 11111111 binary numbers
5. def symbol_32_127(self): return a list of 32 to 127 symbol

### code snippets

```python
from .asciitable import Dec, Oct

class Win1252:
     def dec_0_255(self):
        """return a list of 0 to 255"""
        result = list(Dec().code(256))
        return result

    def oct_000_377(self):
        """return a list of 0 to 377 octal"""
        result = [x["oct"] for x in Oct().code(378)]
        return result

```

