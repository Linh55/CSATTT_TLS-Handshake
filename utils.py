import random

# =========================
# GCD - Euclid
# =========================
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# =========================
# Extended Euclid
# tìm nghịch đảo modulo
# =========================
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def modinv(e, phi):
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise Exception("Không tồn tại nghịch đảo modulo")
    return x % phi


# =========================
# Kiểm tra số nguyên tố
# (đủ dùng cho demo)
# =========================
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0 and n != 2:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# =========================
# Sinh số nguyên tố nhỏ
# =========================
def generate_prime(min_val=100, max_val=300):
    while True:
        num = random.randint(min_val, max_val)
        if is_prime(num):
            return num