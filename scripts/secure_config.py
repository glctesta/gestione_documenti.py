# scripts/secure_config.py
from cryptography.fernet import Fernet
import base64
import os
from pathlib import Path


def generate_key():
    """Genera una chiave di cifratura"""
    key = Fernet.generate_key()
    print(f"Chiave generata: {key.decode()}")
    return key


def encrypt_password(password, key):
    """Cifra una password"""
    cipher = Fernet(key)
    encrypted = cipher.encrypt(password.encode())
    return encrypted.decode()


def setup_secure_config():
    """Setup iniziale per la configurazione sicura"""
    print("=== SETUP CONFIGURAZIONE SICURA ===")

    # Genera chiave
    key = generate_key()
    print("\nAggiungi questa chiave al file .env.db:")
    print(f"ENCRYPTION_KEY={key.decode()}")

    # Chiedi la password del database
    password = input("\nInserisci la password del database: ")

    # Cifra la password
    encrypted_pwd = encrypt_password(password, key)
    print(f"\nPassword cifrata: {encrypted_pwd}")
    print("\nAggiungi questa riga al file .env.db:")
    print(f"DB_PWD_ENCRYPTED={encrypted_pwd}")
    print("\nRimuovi la riga DB_PWD dal file .env.db se presente!")


if __name__ == "__main__":
    setup_secure_config()