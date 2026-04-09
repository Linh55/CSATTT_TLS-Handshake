from aes_core import *
from aes_key_expansion import key_expansion

def pad(data: bytes) -> bytes:
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def split_blocks(data: bytes) -> list[bytes]:
    return [data[i:i+16] for i in range(0, len(data), 16)]

def encrypt_block(plaintext, key):
    # đảm bảo plaintext là bytes
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    # đảm bảo key là bytes
    if isinstance(key, str):
        key = key.encode()

    assert len(plaintext) == 16, f"Plaintext block must be 16 bytes, got {len(plaintext)}"
    assert len(key) == 16, f"Key must be 16 bytes, got {len(key)}"

    state = list(plaintext)   # luôn là list[int]
    key = list(key)

    round_keys = key_expansion(key)

    state = add_round_key(state, round_keys[0])

    for i in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[i])

    # round cuối
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])

    return state

def encrypt(plaintext, key):
    # chuyển về bytes nếu là string
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    if isinstance(key, list):
        key = bytes(key)

    if isinstance(key, str):
        key = key.encode()

    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")

    # padding
    plaintext = pad(plaintext)

    # chia block
    blocks = split_blocks(plaintext)

    cipher = []

    for block in blocks:
        encrypted_block = encrypt_block(block, key)
        cipher.extend(encrypted_block)

    return cipher