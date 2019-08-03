def parse(c):
    if c in ['a', 'b', 'c', 'd', 'e', 'f']:
        return ord(c) - 87
    else:
        return int(c)


def hex_to_int(hex):
    number = 0
    for c, v in enumerate(reversed(hex)):
        number += (parse(v) << (c*4))
    return number

hex1 = input()
hex2 = input()
num1, num2 = hex_to_int(hex1), hex_to_int(hex2)
print(format((num1^num2), 'x'))