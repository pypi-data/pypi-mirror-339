import hashlib

def hash_key(key: str) -> bytes:
    sha1 = hashlib.sha1(key.encode()).digest()
    sha256 = hashlib.sha256(key.encode()).digest()
    sha512 = hashlib.sha512(key.encode()).digest()

    combined = sha1 + sha256 + sha512
    return combined

def generate_patterns(key: str, num_patterns: int = 100) -> list:
    hash_data = hash_key(key)
    patterns = []
    offset = 0

    for i in range(num_patterns):
        length = (hash_data[offset] % 62) + 3
        pattern = hash_data[offset:offset + length]

        if len(pattern) < length:
            pattern += hash_data[:length - len(pattern)]

        patterns.append(list(pattern))
        offset = (offset + length) % len(hash_data)

    return patterns
