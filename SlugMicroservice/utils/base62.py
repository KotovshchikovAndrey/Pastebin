BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(number: int) -> str:
    if number < 0:
        raise ValueError("Invalid number argument. Expected positive int")

    if number == 0:
        return "0"

    base62_string = ""
    while number != 0:
        base62_char = BASE62[number % 62]
        base62_string += base62_char
        number = number // 62

    return base62_string[::-1]


def decode_base62(string: str) -> int:
    if not string:
        raise ValueError("Invalid string argument. Excpected NOT EMPTY string")

    number = 0
    for index, char in enumerate(string[::-1]):
        remain = BASE62.find(char)
        if remain == -1:
            raise ValueError("Invalid char '%s'" % char)

        number += remain * 62**index

    return number
