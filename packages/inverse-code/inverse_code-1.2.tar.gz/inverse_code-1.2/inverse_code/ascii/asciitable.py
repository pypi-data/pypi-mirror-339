"""
`ASCII Table`\n
Reference to ASCII Table of Windows-1252\n
All functions of this class returns a
[generating iterator](https://docs.python.org/3/glossary.html#term-generator).\n
It seems a normal function, except that contains
`yield` expressions to produce a number of usable values in a loop while.
"""

import dataclasses
from inverse_code.error import (
    NonNumber,
    NonNegativeNumber,
    MaximumNumber,
)


@dataclasses.dataclass
class Dec:
    """Decimal from 0 to 255"""

    def code(self, numb, start=0):
        """
        `numb`: is the amounts of times that the loop will be repeated.\n
        `start`: is the initial loop variable.\n"""
        try:
            validate(numb, 256, start)

            while start < numb:
                yield start
                start += 1
        except TypeError as e:
            raise NonNumber from e


@dataclasses.dataclass
class Oct:
    """Octal from 0 to 377"""

    def __init__(self):
        self.__reset = 0
        self.__resetjump = 0

    def code(self, numb, start=0):
        """
        `numb`: is the amounts of times that the loop will be repeated.\n
        `start`: is the initial loop variable.\n
        `self.__reset`: it is the `octal` control variable that goes from `0 to 7`.\n
        `self.__resetjump`: it is the `octal` control variable that goes from `77 + 23`.\n
        @TODO: `new_start`: return string.\n
        """

        try:
            validate(numb, 378, start)
            new_start = ""

            while start < numb:
                new_start = start
                if start < 8:
                    new_start = "0" + str(start)

                yield {"int": start, "oct": new_start}
                if self.__reset == 7:
                    self.__reset = self.__reset - 8
                    start += 2
                self.__reset += 1
                self.__resetjump += 1

                if self.__resetjump == 64:
                    start += 20
                    self.__resetjump = 0
                start += 1

        except TypeError as e:
            raise NonNumber from e


@dataclasses.dataclass
class Hex:
    """Hexadeciaml from 0 to ff"""

    def __init__(self):
        self.__char = ["a", "b", "c", "d", "e", "f"]
        self.__num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.__index_char = {"dynamic": 0, "static": 0}
        self.__index_num = 0
        self.__n = 0
        self.__start = 0
        self.__result = "0"

    def code(self, numb):
        """
        @NOTE: This generator returns a list of each `hexadecimal character` to its implementation
            is a little complex. It was divided into 2 sub methods from 0 to 100 and 101 to 256.\n
        `numb`: number of times that will be repeated.\n
        `self.__start`: it is the loop accountant.\n
        `self.__char[]` : it is the list of characters that will be implemented if you attach this\n
            condition (`if self.__n > 9 and self.__n <= 15`).\n
        `self.__n` : is the variable of hexadecimal control from `0 to 9` and from `a to f`
            that total `15 characters`. \n
        `self.__index_char{}` : is a dictionary that controls the `dynamic` and `static`
            of each hexadecimal number.\n
            that goes from [0 to 5].\n
        `self.__index_num`: is the `index` that controls the `self.__num`'s list
            that goes from [0 to 9].\n
        `self.__result`: returns the result of each `character in string`.\n
        `yield`: returns 1 dictionary of 2 values {int, str}.\n

        ### demonstration

        self.__start = 0\n
        numb = 15

        1. output of the first sequence from [0 to 100]
        - ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0a', '0b', '0c', '0d', '0e', '0f']
        2. output of the second sequence from [101 to 197]
        - ['a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','aa','ab','ac','ad','ae','af']
        ```
        """
        try:

            validate(numb, 197)

            while self.__start < numb:
                if self.__start < 101:
                    # 0 to 100 sequence from [0 to 9] from [a to f] ex.: 0a,0b,0c,0d,0e,0f
                    self.__hexadecimal_0_to_100()
                else:
                    # 100 to 256 sequence from [a to f] from [0 to 9] ex.: a0,a1,a2,a3,a4,05
                    self.__hexadecimal_100_to_256()
                self.__start += 1

                yield {"int": self.__start, "hex": self.__result}
        except TypeError as e:
            raise NonNumber from e

    def __hexadecimal_0_to_100(self):
        if self.__n > 9 and self.__n <= 15:
            self.__result = (
                str(self.__num[self.__index_num])
                + self.__char[self.__index_char["dynamic"]]
            )
            self.__start -= 1
            self.__index_char["dynamic"] += 1
        if self.__n == 17:
            self.__n = 1
            self.__index_num += 1
            self.__index_char["dynamic"] = 0
        if self.__index_num > 9:
            self.__index_num = 0
        if self.__n <= 9 or self.__n > 15:
            if self.__start <= 9:
                self.__result = "0" + str(
                    self.__start
                )  # increases zeros up to 9 the numbers of less than 10.
            else:
                self.__result = str(self.__start)
        if (
            self.__start == 99 and self.__n == 15
        ):  # the first sequence ends and the data restarts
            self.__index_char["dynamic"] = 0
            self.__index_num = 0
            self.__n = 0
            self.__start += 1
        self.__n += 1

    def __hexadecimal_100_to_256(self):
        if self.__n > 10 and self.__n < 17:
            self.__result = (
                self.__char[self.__index_char["static"]]
                + self.__char[self.__index_char["dynamic"]]
            )
            self.__index_char["dynamic"] += 1
        if self.__n == 17:
            self.__n = 1
            self.__index_char["dynamic"] = 0
            self.__index_num = 0
            self.__index_char["static"] += 1
        if self.__n < 11:
            self.__result = self.__char[self.__index_char["static"]] + str(
                self.__num[self.__index_num]
            )
            self.__index_num += 1
        self.__n += 1


@dataclasses.dataclass
class Bin:
    """
    binary from 00000000 to 11111111
    ### base (2)^x
    2⁷, 2⁶, 2⁵, 2⁴, 2³, 2², 2¹, 2⁰\n
    128, 64, 32, 16, 8, 4, 2, 1
    """

    def __init__(self):
        self.__start = 0
        self.__bit = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0}
        self.__num = {
            "n0": 0,
            "n1": 0,
            "n2": 0,
            "n3": 0,
            "n4": 0,
            "n5": 0,
            "n6": 0,
            "n7": 0,
        }

    def code(self, numb):
        """
        @NOTE: This method was divided into 7 submitted to treat each binary number.\n
        `numb`: number of times that will be repeated.\n
        `self.__start`:  it is the loop accountant.\n
        `self.__bit{}`: represents each binary number that goes from `0 to 1`.\n
        `self.__num{}`: is the control variable of each binary number.\n
        `result`: returns the result of each `8bits` binary number.\n
        `yield`: returns 1 dictionary of 2 values {int, str}
        """
        try:
            validate(numb, 256)

            while self.__start < numb:
                self.__binary_h()
                self.__binary_g()
                self.__binary_f()
                self.__binary_e()
                self.__binary_d()
                self.__binary_c()
                self.__binary_b()
                self.__binary_a()

                result = (
                    str(self.__bit["a"])
                    + str(self.__bit["b"])
                    + str(self.__bit["c"])
                    + str(self.__bit["d"])
                    + str(self.__bit["e"])
                    + str(self.__bit["f"])
                    + str(self.__bit["g"])
                    + str(self.__bit["h"])
                )
                self.__num["n1"] += 1
                self.__num["n2"] += 1
                self.__num["n3"] += 1
                self.__num["n4"] += 1
                self.__num["n5"] += 1
                self.__num["n6"] += 1
                self.__num["n7"] += 1
                self.__start += 1
                yield {"int": self.__start, "bin": result}
        except TypeError as e:
            raise NonNumber from e

    def __binary_h(self):
        if self.__num["n0"] < 1:  # H
            self.__bit["h"] = 0
            self.__num["n0"] += 1
        else:
            self.__bit["h"] = 1
            self.__num["n0"] = 0

    def __binary_g(self):
        if self.__num["n1"] < 2:  # G
            self.__bit["g"] = 0
        else:
            self.__bit["g"] = 1
            if self.__num["n1"] == 3:
                self.__num["n1"] = self.__num["n1"] - 4

    def __binary_f(self):
        if self.__num["n2"] < 4:  # F
            self.__bit["f"] = 0
        else:
            self.__bit["f"] = 1
            if self.__num["n2"] == 7:
                self.__num["n2"] = self.__num["n2"] - 8

    def __binary_e(self):
        if self.__num["n3"] < 8:  # E
            self.__bit["e"] = 0
        else:
            self.__bit["e"] = 1
            if self.__num["n3"] == 15:
                self.__num["n3"] = self.__num["n3"] - 16

    def __binary_d(self):
        if self.__num["n4"] < 16:  # D
            self.__bit["d"] = 0
        else:
            self.__bit["d"] = 1
            if self.__num["n4"] == 31:
                self.__num["n4"] = self.__num["n4"] - 32

    def __binary_c(self):
        if self.__num["n5"] < 32:  # C
            self.__bit["c"] = 0
        else:
            self.__bit["c"] = 1
            if self.__num["n5"] == 63:
                self.__num["n5"] = self.__num["n5"] - 64

    def __binary_b(self):
        if self.__num["n6"] < 64:  # B
            self.__bit["b"] = 0
        else:
            self.__bit["b"] = 1
            if self.__num["n6"] == 127:
                self.__num["n6"] = self.__num["n6"] - 128

    def __binary_a(self):
        if self.__num["n7"] < 128:  # A
            self.__bit["a"] = 0
        else:
            self.__bit["a"] = 1
            if self.__num["n7"] == 255:
                self.__num["n7"] = self.__num["n7"] - 256


@dataclasses.dataclass
class Symbol:
    """Symbol from 32 to 127"""

    def __init__(self):
        self.__start = 0
        self.__symbol = [
            "nul",
            "soh",
            "stx",
            "etx",
            "eot",
            "enq",
            "ack",
            "bel",
            "bs",
            "ht",
            "lf",
            "vf",
            "ff",
            "cr",
            "so",
            "si",
            "dle",
            "dc1",
            "dc2",
            "dc3",
            "dc4",
            "nak",
            "syn",
            "etb",
            "can",
            "em",
            "sub",
            "esc",
            "fs",
            "gs",
            "rs",
            "us",
            " ",
            "!",
            '"',
            "#",
            "$",
            "%",
            "&",
            "'",
            "(",
            ")",
            "*",
            "+",
            ",",
            "-",
            ".",
            "/",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            ":",
            ";",
            "<",
            "=",
            ">",
            "?",
            "@",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "[",
            "\\",
            "]",
            "^",
            "_",
            "`",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "{",
            "|",
            "}",
            "~",
            "del",
        ]

    def code(self, numb):
        """
        `numb`: number of times that will be repeated.\n
        `self.__start`: it is the loop accountant.\n
        `self.__symbol[]: it's a list of symbols.\n
        `self.__result`: returns the result of each `8bits` binary number.\n
        """
        try:
            validate(numb, 128)
            while self.__start < numb:
                result = self.__symbol[self.__start]
                self.__start += 1
                yield {"int": self.__start, "symb": result}
        except TypeError as e:
            raise NonNumber from e


def validate(numb, max_number, start=0):
    """validation of [`numb, max number` and `start`]"""
    if numb < 1:
        raise NonNegativeNumber

    if numb > max_number:
        raise MaximumNumber(max_number)

    if start < 0:
        raise NonNegativeNumber
