import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SALT = b'vaultsafe_salt_123'  # You can replace this with os.urandom(16)

def generate_key_from_password(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_note(note_text: str, password: str) -> bytes:
    key = generate_key_from_password(password)
    return Fernet(key).encrypt(note_text.encode())

def decrypt_note(cipher_text: bytes, password: str) -> str:
    try:
        key = generate_key_from_password(password)
        return Fernet(key).decrypt(cipher_text).decode()
    except Exception:
        return "❌ Decryption Failed"

def encrypt_file(file_obj, password: str) -> bytes:
    key = generate_key_from_password(password)
    return Fernet(key).encrypt(file_obj.read())

def decrypt_file(file_path: str, password: str) -> bytes:
    try:
        with open(file_path, 'rb') as f:
            encrypted = f.read()
        key = generate_key_from_password(password)
        return Fernet(key).decrypt(encrypted)
    except Exception:
        return None
