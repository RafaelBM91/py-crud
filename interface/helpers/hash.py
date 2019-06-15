from hashlib import sha256

def crypt(key):
    return sha256(key.encode()).hexdigest()
