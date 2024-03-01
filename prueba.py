import random as rn
from random import shuffle,choice
import string

def generate_password():
    all  = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits)
    shuffle(all)
    new_password = ''

    for _ in range(10):
        new_password += choice(all)
    return new_password

print(generate_password())