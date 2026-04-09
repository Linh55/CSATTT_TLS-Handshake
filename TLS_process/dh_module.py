import random
from utils import generate_prime

# =========================
# Sinh tham số DH
# =========================
def generate_params():
    # dùng số nguyên tố nhỏ cho demo
    p = generate_prime(200, 500)
    g = random.randint(2, p - 2)
    return p, g


# =========================
# Private key
# =========================
def generate_private_key(p):
    return random.randint(2, p - 2)


# =========================
# Public key
# =========================
def compute_public_key(g, private_key, p):
    return pow(g, private_key, p)


# =========================
# Shared secret
# =========================
def compute_shared_key(public_key, private_key, p):
    return pow(public_key, private_key, p)