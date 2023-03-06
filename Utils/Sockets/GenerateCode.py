import random


def generateCode(length: int) -> str:
    response = ''

    while (length := length - 1) > 0:
        random_char = random.randint(48, 122)

        if 58 <= random_char <= 64:
            length += 1
        else:
            response += chr(random_char)

    return response
