import random

def gen_pass(pass_length):
    elements = "qwertyuiop[]asdfghjkl;'\zxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,./+-!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

def gen_coin():
    coin = random.randint(0, 1)
    coin_result = ''
    if coin == 0:
        coin_result = 'Решка'
    else:
        coin_result = 'Орёл'

    return coin_result