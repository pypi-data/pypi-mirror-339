def decode(ciphertext: bytes, patterns: list[list[int]]) -> str:
    data = list(ciphertext)

    for pattern in reversed(patterns):
        for i in range(len(data)):
            data[i] = (data[i] - pattern[i % len(pattern)]) % 256

    return bytes(data).decode()
