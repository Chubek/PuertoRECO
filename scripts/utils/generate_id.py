import random


def generate_random_str():
    MAX_LIMIT = 255

    random_string = ''

    for _ in range(5):
        random_integer = random.randint(0, MAX_LIMIT)
        random_string += (chr(random_integer))

    return random_string