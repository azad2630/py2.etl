import os
import base64
import pandas as pd

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# VALG AF METODE
# Jeg vælger AES-GCM til denne datapipeline.
# Begrundelse:
# - CSV- og database-data er tekst/tabulære værdier.
# - AES-GCM giver både fortrolighed og integritet i én operation.
# - Det er mere sikkert og enklere end ren AES-CBC, som kræver ekstra
#   beskyttelse mod manipulation.
# - Fernet er også sikkert, men AES-GCM er mere direkte og velegnet til
#   felt-for-felt kryptering i denne type ETL-pipeline.


DEFAULT_METHOD = "aes_gcm"


def get_aes_key():
    key_b64 = os.getenv("APP_AES_KEY_B64")
    if not key_b64:
        raise ValueError("Missing environment variable APP_AES_KEY_B64")
    return base64.urlsafe_b64decode(key_b64)


def get_fernet_key():
    key = os.getenv("APP_FERNET_KEY")
    if not key:
        raise ValueError("Missing environment variable APP_FERNET_KEY")
    return key.encode()


# AES-GCM

def encrypt_aes_gcm(plaintext):
    key = get_aes_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    token = base64.urlsafe_b64encode(nonce + ciphertext).decode("utf-8")
    return token


def decrypt_aes_gcm(token):
    key = get_aes_key()
    aesgcm = AESGCM(key)

    data = base64.urlsafe_b64decode(token.encode("utf-8"))
    nonce = data[:12]
    ciphertext = data[12:]

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


# AES-CBC

def encrypt_aes_cbc(plaintext):
    key = get_aes_key()
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    token = base64.urlsafe_b64encode(iv + ciphertext).decode("utf-8")
    return token


def decrypt_aes_cbc(token):
    key = get_aes_key()
    data = base64.urlsafe_b64decode(token.encode("utf-8"))

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode("utf-8")


# Fernet

def encrypt_fernet(plaintext):
    f = Fernet(get_fernet_key())
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_fernet(token):
    f = Fernet(get_fernet_key())
    plaintext = f.decrypt(token.encode("utf-8"))
    return plaintext.decode("utf-8")


# Standard-wrapper

def encrypt_value(value, method=DEFAULT_METHOD):
    text = str(value)

    if method == "aes_gcm":
        return encrypt_aes_gcm(text)
    elif method == "aes_cbc":
        return encrypt_aes_cbc(text)
    elif method == "fernet":
        return encrypt_fernet(text)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")


def decrypt_value(value, method=DEFAULT_METHOD):
    if method == "aes_gcm":
        return decrypt_aes_gcm(value)
    elif method == "aes_cbc":
        return decrypt_aes_cbc(value)
    elif method == "fernet":
        return decrypt_fernet(value)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")


def encrypt_dataframe(df, method=DEFAULT_METHOD):
    encrypted_df = df.copy()
    for col in encrypted_df.columns:
        encrypted_df[col] = encrypted_df[col].apply(lambda x: encrypt_value(x, method))
    return encrypted_df


def decrypt_dataframe(df, method=DEFAULT_METHOD):
    decrypted_df = df.copy()
    for col in decrypted_df.columns:
        decrypted_df[col] = decrypted_df[col].apply(lambda x: decrypt_value(x, method))
    return decrypted_df


def cast_iris_columns(df):
    numeric_columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col])

    return df