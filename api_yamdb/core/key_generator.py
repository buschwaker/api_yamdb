import string
import random


def generate_alphanum_random_string(length):
    """Генерация кода подтверждения длиной length"""
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string
