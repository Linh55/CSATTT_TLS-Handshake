from aes_core import S_BOX

RCON = [0x01, 0x02, 0x04, 0x08, 0x10,
        0x20, 0x40, 0x80, 0x1B, 0x36]

def key_expansion(key):
    # key: list 16 bytes
    expanded = key[:]   # 16 bytes ban đầu

    i = 4
    while len(expanded) < 176:
        temp = expanded[-4:]  # lấy 4 byte cuối

        if i % 4 == 0:
            # rotate
            temp = temp[1:] + temp[:1]

            # subbytes
            temp = [S_BOX[b] for b in temp]

            # XOR với RCON
            temp[0] ^= RCON[(i // 4) - 1]

        # XOR với word trước đó (cách 16 bytes)
        prev = expanded[-16:-12]

        new_word = [t ^ p for t, p in zip(temp, prev)]

        expanded.extend(new_word)

        i += 1

    # chia thành round keys (11 keys)
    return [expanded[i:i+16] for i in range(0, 176, 16)]