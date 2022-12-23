import random


def random_string(length: int = 8):
    s = "0123456789abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choices(s, k=length))
