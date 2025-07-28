from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

# Load or generate key
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

cipher = Fernet(key)

def encrypt(plain_text: str) -> str:
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt(encrypted_text: str) -> str:
    return cipher.decrypt(encrypted_text.encode()).decode()