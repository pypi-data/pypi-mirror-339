# Inverse code

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![pypi: version](https://img.shields.io/badge/pypi-25.0.1-blue)](https://pypi.org/project/pip/)
[![python: version](https://img.shields.io/badge/python-3.13.2-blue)](https://docs.python.org/)
[![unittest](https://img.shields.io/badge/doctest-unittest-red)](https://docs.python.org/3/library/unittest.html)
[![ascii](https://img.shields.io/badge/ascii-windows1252-purple)](https://www.ascii-code.com/)
[![pyproject: toml](https://img.shields.io/badge/pyproject-toml-white)](https://packaging.python.org/en/latest/guides/writing-pyproject/)
[![twine](https://img.shields.io/badge/twine-utility-brown)](https://pypi.org/project/twine/)


Reverse Code is a library created for Python to help developers encrypt and retrieve their data in a simple and dynamic way.

This cryptography is at least vaguely similar to real-world things, such as `Reed-Solomon error correction` codes or some interspersed data formats that can be transmitted by `IoT` edge devices.

`ASCII`, means American standard code for information exchange. It is a 7 -bit character code where each individual bit represents a unique character.

I used the 8-bit ASCII table with 256 characters and symbols, which is based on the Windows-1252 characters set.

### Data processing provided in unusual formats or owners
For the success of this library was divided into some sub library:
- [ascii](https://github.com/aniceto-jolela/inverse_code/blob/main/inverse_code/ascii/ASCII.md)
- [convert](https://github.com/aniceto-jolela/inverse_code/blob/main/inverse_code/convert/CONVERT.md)
- [helpers](https://github.com/aniceto-jolela/inverse_code/blob/main/inverse_code/helpers/HELPERS.md)

### Example of encryption. 
>>> ### Encode 
>>> character = "FRED" <br>
converts_character_to_binary = ['01000100', '01000101', '01010010', '01000110'] <br>
increases_4_bits_up_to_32_bits = [['0', '1', '0', '0', '0', '1', '0', '0'],['0', '1', '0', '0', '0', '1', '0', '1'],['0', '1', '0', '1', '0', '0', '1', '0'],['0', '1', '0', '0', '0', '1', '1', '0']] <br>
encodes_bit_a_bit = [['0', '1', '0', '0', '0', '1', '0', '0'],['0', '1', '0', '0', '0', '1', '0', '1'],['0', '1', '0', '1', '0', '0', '1', '0'],['0', '1', '0', '0', '0', '1', '1', '0']] <br>
reduce_to_4_bits_again = ['00001111', '00000010', '00001101', '00110100'] <br>
converts_binary_to_hexadecimal =  ['0f', '02', '0d', '34'] <br>
converts_decimal = 251792692 <br>

```python
from inverse_code import encode

symbol = encode.encode("FRED")

print(symbol) #out of the code : 251792692
```

>>> ### Decode 
>>> decimal_number = 251792692 <br/>
converts_decimal_hexadecimal = ['0f', '02', '0d', '34'] <br/>
converts_hexadecimal_binary = ['00001111', '00000010', '00001101', '00110100'] <br/>
increases_4_bits_up_to_32_bits = [['0', '0', '0', '0', '1', '1', '1', '1'], ['0', '0', '0', '0', '0', '0', '1', '0'], ['0', '0', '0', '0', '1', '1', '0', '1'], ['0', '0', '1', '1', '0', '1', '0', '0']] <br/>
reduce_to_4_bits_again = ['01000100', '01000101', '01010010', '01000110'] <br/>
converts_binary_symbol = 'FRED' <br/>

```python
from inverse_code import decode

symbol = decode.decode(251792692)

print(symbol)  # out of the code : FRED
```

### Project structure
inverse_code <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +---[inverse_code](https://github.com/aniceto-jolela/inverse_code/blob/main/inverse_code/INVERSE_CODE.md) <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---ascii <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---ASCII.md <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+--- ... <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---convert <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---CONVERT.md <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+--- ... <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---helpers <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---HELPERS.md <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+--- ... <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +---tests <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---test_convert <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---test_ascii <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---test_helpers <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---test_encode.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---test_decode.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+--- ... <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +---.pylintrc <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +---README.md <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +---setup.py <br/>

> [!IMPORTANT] 
> I avoided 98.7% the use of libraries or third party structures, because one of the goals is to help and see how my code can be amazing when I am working on a problem where none of these libraries still exist.
#

### Convert

> Decimal
```python
from inverse_code.convert import cdec

binary = cdec.cdec_binary(63)
octal = cdec.cdec_octal(63)
hexadecimal = cdec.cdec_hexadecimal(63)
symbol = cdec.cdec_symbol(63)

print(binary)  # out of the code : 00111111
print(octal)  # out of the code : 77
print(hexadecimal)  # out of the code : 3f
print(symbol)  # out of the code : ?

```
> Octal
```python
from inverse_code.convert import coct

decimal = coct.coct_decimal(155)
binary = coct.coct_binary(155)
hexadecimal = coct.coct_hexadecimal(155)
symbol = coct.coct_symbol(155)

print(decimal)  # out of the code : 109
print(binary)  # out of the code : 01101101
print(hexadecimal)  # out of the code : 6d
print(symbol)  # out of the code : m
```
> Hexadecimal
```python
from inverse_code.convert import chex

decimal = chex.chex_decimal("2d")
binary = chex.chex_binary("2d")
octal = chex.chex_octal("2d")
symbol = chex.chex_symbol("2d")

print(decimal)  # out of the code : 45
print(binary)  # out of the code : 00101101
print(octal)  # out of the code : 55
print(symbol)  # out of the code : -
```
> Binary
```python
from inverse_code.convert import cbin

decimal = cbin.cbin_decimal("01111110")
hexadecimal = cbin.cbin_hexadecimal("01111110")
octal = cbin.cbin_octal("01111110")
symbol = cbin.cbin_symbol("01111110")

print(decimal)  # out of the code : 126
print(hexadecimal)  # out of the code : 7e
print(octal)  # out of the code : 176
print(symbol)  # out of the code : ~
```
> Symbol
```python
from inverse_code.convert import csymb

decimal = csymb.csymb_decimal("p")
hexadecimal = csymb.csymb_hexadecimal("p")
octal = csymb.csymb_octal("p")
binary = csymb.csymb_binary("p")

print(decimal)  # out of the code : 112
print(hexadecimal)  # out of the code : 70
print(octal)  # out of the code : 160
print(binary)  # out of the code : 01110000
```

### Helpers

> Decimal
```python
from inverse_code.helpers import decshow

decimal_control_characters = decshow.control_characters_0_31()
decimal_printable_characters = decshow.printable_characters_32_127()
decimal_extended_ascii = decshow.extended_ascii_128_255()
decimal_all = decshow.all_decimal()

print(decimal_control_characters)  # out of the code : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

print(decimal_printable_characters)  # out of the code : [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]

print(decimal_extended_ascii)  # out of the code : [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

print(decimal_all)  # out of the code : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

```
> Octal
```python
from inverse_code.helpers import octshow

octal_control_characters = octshow.control_characters_0_37()
octal_printable_characters = octshow.printable_characters_40_177()
octal_extended_ascii = octshow.extended_ascii_200_377()
octal_all = octshow.all_octal()

print(octal_control_characters)  # out of the code : ['00', '01', '02', '03', '04', '05', '06', '07', 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 37]

print(octal_printable_characters)  # out of the code : [40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86, 87, 90, 91, 92, 93, 94, 95, 96, 97, 100, 101, 102, 103, 104, 105, 106, 107, 110, 111, 112, 113, 114, 115, 116, 117, 140, 141, 142, 143, 144, 145, 146, 147, 150, 151, 152, 153, 154, 155, 156, 157, 160, 161, 162, 163, 164, 165, 166, 167, 170, 171, 172, 173, 174, 175, 176, 177]

print(octal_extended_ascii)  # out of the code : [200, 201, 202, 203, 204, 205, 206, 207, 210, 211, 212, 213, 214, 215, 216, 217, 220, 221, 222, 223, 224, 225, 226, 227, 230, 231, 232, 233, 234, 235, 236, 237, 240, 241, 242, 243, 244, 245, 246, 247, 250, 251, 252, 253, 254, 255, 256, 257, 260, 261, 262, 263, 264, 265, 266, 267, 270, 271, 272, 273, 274, 275, 276, 277, 300, 301, 302, 303, 304, 305, 306, 307, 310, 311, 312, 313, 314, 315, 316, 317, 320, 321, 322, 323, 324, 325, 326, 327, 330, 331, 332, 333, 334, 335, 336, 337, 340, 341, 342, 343, 344, 345, 346, 347, 350, 351, 352, 353, 354, 355, 356, 357, 360, 361, 362, 363, 364, 365, 366, 367, 370, 371, 372, 373, 374, 375, 376, 377]

print(octal_all)  # out of the code : ['00', '01', '02', '03', '04', '05', '06', '07', 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 37, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 76, 77, 100, 101, 102, 103, 104, 105, 106, 107, 110, 111, 112, 113, 114, 115, 116, 117, 120, 121, 122, 123, 124, 125, 126, 127, 130, 131, 132, 133, 134, 135, 136, 137, 140, 141, 142, 143, 144, 145, 146, 147, 150, 151, 152, 153, 154, 155, 156, 157, 160, 161, 162, 163, 164, 165, 166, 167, 170, 171, 172, 173, 174, 175, 176, 177, 200, 201, 202, 203, 204, 205, 206, 207, 210, 211, 212, 213, 214, 215, 216, 217, 220, 221, 222, 223, 224, 225, 226, 227, 230, 231, 232, 233, 234, 235, 236, 237, 240, 241, 242, 243, 244, 245, 246, 247, 250, 251, 252, 253, 254, 255, 256, 257, 260, 261, 262, 263, 264, 265, 266, 267, 270, 271, 272, 273, 274, 275, 276, 277, 300, 301, 302, 303, 304, 305, 306, 307, 310, 311, 312, 313, 314, 315, 316, 317, 320, 321, 322, 323, 324, 325, 326, 327, 330, 331, 332, 333, 334, 335, 336, 337, 340, 341, 342, 343, 344, 345, 346, 347, 350, 351, 352, 353, 354, 355, 356, 357, 360, 361, 362, 363, 364, 365, 366, 367, 370, 371, 372, 373, 374, 375, 376, 377]

```
> Hexadecimal
```python
from inverse_code.helpers import hexshow

hexadecimal_control_characters = hexshow.control_characters_0_1f()
hexadecimal_printable_characters = hexshow.printable_characters_20_7f()
hexadecimal_extended_ascii = hexshow.extended_ascii_80_ff()
hexadecimal_all = hexshow.all_hexadecimal()

print(hexadecimal_control_characters)  # out of the code : ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f']

print(hexadecimal_printable_characters)  # out of the code : ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']

print(hexadecimal_extended_ascii)  # out of the code : ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']

print(hexadecimal_all)  # out of the code : ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']

```
> Symbol
```python
from inverse_code.helpers import symbshow

symbol_control_characters = symbshow.printable_characters_32_127()
symbol_all = symbshow.all_symbol()

print(symbol_control_characters)  # out of the code : [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'del']

print(symbol_all)  # out of the code : ['nul', 'soh', 'stx', 'etx', 'eot', 'enq', 'ack', 'bel', 'bs', 'ht', 'lf', 'vf', 'ff', 'cr', 'so', 'si', 'dle', 'dc1', 'dc2', 'dc3', 'dc4', 'nak', 'syn', 'etb', 'can', 'em', 'sub', 'esc', 'fs', 'gs', 'rs', 'us', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'del']
```
> Binary
```python
from inverse_code.helpers import binshow

binary_control_characters = binshow.control_characters_0_11111()
binary_printable_characters = binshow.printable_characters_100000_01111111()
binary_extended_ascii = binshow.extended_ascii_10000000_11111111()
binary_all = binshow.all_binary()

print(binary_control_characters)  # out of the code : ['00000000', '00000001', '00000010', '00000011', '00000100', '00000101', '00000110', '00000111', '00001000', '00001001', '00001010', '00001011', '00001100', '00001101', '00001110', '00001111', '00010000', '00010001', '00010010', '00010011', '00010100', '00010101', '00010110', '00010111', '00011000', '00011001', '00011010', '00011011', '00011100', '00011101', '00011110', '00011111']

print(binary_printable_characters)  # out of the code : ['00100000', '00100001', '00100010', '00100011', '00100100', '00100101', '00100110', '00100111', '00101000', '00101001', '00101010', '00101011', '00101100', '00101101', '00101110', '00101111', '00110000', '00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000', '00111001', '00111010', '00111011', '00111100', '00111101', '00111110', '00111111', '01000000', '01000001', '01000010', '01000011', '01000100', '01000101', '01000110', '01000111', '01001000', '01001001', '01001010', '01001011', '01001100', '01001101', '01001110', '01001111', '01010000', '01010001', '01010010', '01010011', '01010100', '01010101', '01010110', '01010111', '01011000', '01011001', '01011010', '01011011', '01011100', '01011101', '01011110', '01011111', '01100000', '01100001', '01100010', '01100011', '01100100', '01100101', '01100110', '01100111', '01101000', '01101001', '01101010', '01101011', '01101100', '01101101', '01101110', '01101111', '01110000', '01110001', '01110010', '01110011', '01110100', '01110101', '01110110', '01110111', '01111000', '01111001', '01111010', '01111011', '01111100', '01111101', '01111110', '01111111']

print(binary_extended_ascii)  # out of the code : ['10000000', '10000001', '10000010', '10000011', '10000100', '10000101', '10000110', '10000111', '10001000', '10001001', '10001010', '10001011', '10001100', '10001101', '10001110', '10001111', '10010000', '10010001', '10010010', '10010011', '10010100', '10010101', '10010110', '10010111', '10011000', '10011001', '10011010', '10011011', '10011100', '10011101', '10011110', '10011111', '10100000', '10100001', '10100010', '10100011', '10100100', '10100101', '10100110', '10100111', '10101000', '10101001', '10101010', '10101011', '10101100', '10101101', '10101110', '10101111', '10110000', '10110001', '10110010', '10110011', '10110100', '10110101', '10110110', '10110111', '10111000', '10111001', '10111010', '10111011', '10111100', '10111101', '10111110', '10111111', '11000000', '11000001', '11000010', '11000011', '11000100', '11000101', '11000110', '11000111', '11001000', '11001001', '11001010', '11001011', '11001100', '11001101', '11001110', '11001111', '11010000', '11010001', '11010010', '11010011', '11010100', '11010101', '11010110', '11010111', '11011000', '11011001', '11011010', '11011011', '11011100', '11011101', '11011110', '11011111', '11100000', '11100001', '11100010', '11100011', '11100100', '11100101', '11100110', '11100111', '11101000', '11101001', '11101010', '11101011', '11101100', '11101101', '11101110', '11101111', '11110000', '11110001', '11110010', '11110011', '11110100', '11110101', '11110110', '11110111', '11111000', '11111001', '11111010', '11111011', '11111100', '11111101', '11111110', '11111111']

print(binary_all)  # out of the code : ['00000000', '00000001', '00000010', '00000011', '00000100', '00000101', '00000110', '00000111', '00001000', '00001001', '00001010', '00001011', '00001100', '00001101', '00001110', '00001111', '00010000', '00010001', '00010010', '00010011', '00010100', '00010101', '00010110', '00010111', '00011000', '00011001', '00011010', '00011011', '00011100', '00011101', '00011110', '00011111', '00100000', '00100001', '00100010', '00100011', '00100100', '00100101', '00100110', '00100111', '00101000', '00101001', '00101010', '00101011', '00101100', '00101101', '00101110', '00101111', '00110000', '00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000', '00111001', '00111010', '00111011', '00111100', '00111101', '00111110', '00111111', '01000000', '01000001', '01000010', '01000011', '01000100', '01000101', '01000110', '01000111', '01001000', '01001001', '01001010', '01001011', '01001100', '01001101', '01001110', '01001111', '01010000', '01010001', '01010010', '01010011', '01010100', '01010101', '01010110', '01010111', '01011000', '01011001', '01011010', '01011011', '01011100', '01011101', '01011110', '01011111', '01100000', '01100001', '01100010', '01100011', '01100100', '01100101', '01100110', '01100111', '01101000', '01101001', '01101010', '01101011', '01101100', '01101101', '01101110', '01101111', '01110000', '01110001', '01110010', '01110011', '01110100', '01110101', '01110110', '01110111', '01111000', '01111001', '01111010', '01111011', '01111100', '01111101', '01111110', '01111111', '10000000', '10000001', '10000010', '10000011', '10000100', '10000101', '10000110', '10000111', '10001000', '10001001', '10001010', '10001011', '10001100', '10001101', '10001110', '10001111', '10010000', '10010001', '10010010', '10010011', '10010100', '10010101', '10010110', '10010111', '10011000', '10011001', '10011010', '10011011', '10011100', '10011101', '10011110', '10011111', '10100000', '10100001', '10100010', '10100011', '10100100', '10100101', '10100110', '10100111', '10101000', '10101001', '10101010', '10101011', '10101100', '10101101', '10101110', '10101111', '10110000', '10110001', '10110010', '10110011', '10110100', '10110101', '10110110', '10110111', '10111000', '10111001', '10111010', '10111011', '10111100', '10111101', '10111110', '10111111', '11000000', '11000001', '11000010', '11000011', '11000100', '11000101', '11000110', '11000111', '11001000', '11001001', '11001010', '11001011', '11001100', '11001101', '11001110', '11001111', '11010000', '11010001', '11010010', '11010011', '11010100', '11010101', '11010110', '11010111', '11011000', '11011001', '11011010', '11011011', '11011100', '11011101', '11011110', '11011111', '11100000', '11100001', '11100010', '11100011', '11100100', '11100101', '11100110', '11100111', '11101000', '11101001', '11101010', '11101011', '11101100', '11101101', '11101110', '11101111', '11110000', '11110001', '11110010', '11110011', '11110100', '11110101', '11110110', '11110111', '11111000', '11111001', '11111010', '11111011', '11111100', '11111101', '11111110', '11111111']

```
> Helpers
```python
from inverse_code.helpers import helpers

all_ascii_table = helpers.all_ascii_table()

print(all_ascii_table)  # out of the code : ...
```
#
#
## Project configuration

### Environment
```bash
python -m venv env_inverse_code
```
```bash
source envs/env_inverse_code/bin/activate
```

### Auto-formatting tools and Linting

```python
pip install black
```
```python
pip install pylint[spelling]
```
```
pylint --generate-rcfile > .pylintrc
``` 

### Visual Studio Code - Marketplace

![CRT](https://img.shields.io/badge/Extensions_command-Ctrl+Shift+X-orange?style=plastic)

[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
```bash
ext install ms-python.python
```
[Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
```bash
ext install ms-python.black-formatter
```
[Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
```bash
ext install ms-python.pylint
```
[TODO Highlight](https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight)
```bash
ext install wayou.vscode-todo-highlight
```
