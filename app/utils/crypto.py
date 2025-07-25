from cryptography.fernet import Fernet as fn

key = fn.generate_key()
cipher =  fn(key)

def encrypt(plain_text: bytes) -> bytes:
    return cipher.encrypt(plain_text)

def decrypt(encrypted_text: bytes) -> bytes:
    return cipher.decrypt(encrypted_text)