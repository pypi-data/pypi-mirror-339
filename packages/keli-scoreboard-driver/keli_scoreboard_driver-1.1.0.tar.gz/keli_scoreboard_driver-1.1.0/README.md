# KELI Scoreboard driver

Welcome to my simple KELI scoreboard driver implementation. This driver supports some general characters, 
ukrainian and english alphabets. I used this with KELI DPM-DZ-INT-3, but probably it should work with other series

## Installation 
```sh
pip install keli-scoreboard
```

## Usage

```python
from keli_scoreboard import KeliScoreboard

# Initialize driver instance
driver = KeliScoreboard('/dev/ttyUSB0')

# Print out your custom information or weight
driver.print_text('hello, world!')

for weight in range(1, 1000):
    driver.print_weight(weight)

# Release resources acquired by port usage
driver.close()

# Or you can use context manager
with KeliScoreboard('/dev/ttyUSB0') as scoreboard:
    scoreboard.print_text('Some information')
```

## Error handling
When you're instantiating object or calling any function you can receive SerialPort exception (keli_scoreboard.SerialException).

If you try to use unsupported character, you'll receive KeyError Exception (print_text method)

## Features

This driver implements a particular set of characters (general special symbols, ukrainial letter and latin).
All these characters were found by protocol reverse engineering
```text
Supported characters:
    ' '
    ','
    "'" 
    '='
    '-' 
    ':'
    '?'
    'a'
    'b'
    'c'
    'd'
    'e'
    'f'
    'g'
    'h'
    'i'
    'j'
    'k'
    'l'
    'm'
    'n'
    'o'
    'p'
    'q'
    'r'
    's'
    't'
    'u'
    'v'
    'w'
    'x'
    'y'
    'z'
    'A'
    'B'
    'C'
    'D'
    'E'
    'F'
    'G'
    'H'
    'I'
    'J'
    'K'
    'L'
    'M'
    'N'
    'O'
    'P'
    'Q'
    'R'
    'S'
    'T'
    'U'
    'V'
    'W'
    'X'
    'Y'
    'Z'
    '0'
    '1'
    '2'
    '3'
    '4'
    '5'
    '6'
    '7'
    '8'
    '9'
    'а'
    'б'
    'в'
    'г'
    'д'
    'е'
    'є'
    'ж'
    'з'
    'и'
    'і'
    'ї'
    'й'
    'к'
    'л'
    'м'
    'н'
    'о'
    'п'
    'р'
    'с'
    'т'
    'у'
    'ф'
    'х'
    'ц'
    'ч'
    'ш'
    'щ'
    'ь'
    'ю'
    'я'
    'А'
    'Б'
    'В'
    'Г'
    'Д'
    'Е'
    'Є'
    'Ж'
    'З'
    'И'
    'І'
    'Ї'
    'Й'
    'К'
    'Л'
    'М'
    'Н'
    'О'
    'П'
    'Р'
    'С'
    'Т'
    'У'
    'Ф'
    'Х'
    'Ц'
    'Ч'
    'Ш'
    'Щ'
    'Ь'
    'Ю'
    'Я'
```
