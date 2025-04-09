def encode(text: str, patterns: list[list[int]]) -> bytes:
    data = list(text.encode())

    for pattern in patterns:
        for i in range(len(data)):
            data[i] = (data[i] + pattern[i % len(pattern)]) % 256

    return bytes(data)
