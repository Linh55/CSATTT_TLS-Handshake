import random
from utils import gcd, modinv, generate_prime

# =========================
# Sinh key RSA
# =========================
def generate_keys():
    p = generate_prime()
    q = generate_prime()

    while q == p:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    # chọn e
    e = 65537
    if gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
        while gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)

    d = modinv(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


# =========================
# Chuyển string → int
# =========================
def string_to_int(message):
    return int.from_bytes(message.encode(), 'big')


def int_to_string(number):
    length = (number.bit_length() + 7) // 8
    return number.to_bytes(length, 'big').decode(errors='ignore')


# =========================
# Encrypt / Decrypt
# =========================
def encrypt(message, public_key):
    e, n = public_key
    m = string_to_int(message)
    return pow(m, e, n)


def decrypt(cipher, private_key):
    d, n = private_key
    m = pow(cipher, d, n)
    return int_to_string(m)


# =========================
# Sign / Verify
# =========================
def sign(message, private_key):
    d, n = private_key
    m = string_to_int(message)
    return pow(m, d, n)


def verify(message, signature, public_key):
    e, n = public_key
    m = string_to_int(message)
    return pow(signature, e, n) == m