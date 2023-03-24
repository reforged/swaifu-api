import random


def generateCode(length: int) -> str:
    """
    Permet de générer un code de session aléatoire.
    """
    response = ''

    while (length := length - 1) > 0:
        random_char = random.randint(65, 122)

        if 91 <= random_char <= 96:
            length += 1
        else:
            response += chr(random_char)

    return response
