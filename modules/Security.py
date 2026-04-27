import os
import base64
import pandas as pd

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Valgt standardmetode til kryptering i projektet
# AES-GCM bruges som standard, når der ikke vælges en anden metode
DEFAULT_METHOD = "aes_gcm"


def get_aes_key():
    # Henter AES-nøglen fra miljøvariablen APP_AES_KEY_B64
    key_b64 = os.getenv("APP_AES_KEY_B64")

    # Stopper med fejl hvis nøglen ikke findes
    if not key_b64:
        raise ValueError("Missing environment variable APP_AES_KEY_B64")

    # Dekoder nøglen fra base64-format til bytes
    return base64.urlsafe_b64decode(key_b64)


def get_fernet_key():
    # Henter Fernet-nøglen fra miljøvariablen APP_FERNET_KEY
    key = os.getenv("APP_FERNET_KEY")

    # Stopper med fejl hvis nøglen ikke findes
    if not key:
        raise ValueError("Missing environment variable APP_FERNET_KEY")

    # Konverterer nøglen til bytes
    return key.encode()


def encrypt_aes_gcm(plaintext):
    # Henter AES-nøglen
    key = get_aes_key()

    # Opretter AES-GCM objekt
    aesgcm = AESGCM(key)

    # Genererer en tilfældig nonce på 12 bytes
    nonce = os.urandom(12)

    # Krypterer plaintext efter at den er konverteret til UTF-8 bytes
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

    # Samler nonce og ciphertext og koder det til base64-tekst
    token = base64.urlsafe_b64encode(nonce + ciphertext).decode("utf-8")
    return token


def decrypt_aes_gcm(token):
    # Henter AES-nøglen
    key = get_aes_key()

    # Opretter AES-GCM objekt
    aesgcm = AESGCM(key)

    # Dekoder token fra base64 til bytes
    data = base64.urlsafe_b64decode(token.encode("utf-8"))

    # Splitter data i nonce og ciphertext
    nonce = data[:12]
    ciphertext = data[12:]

    # Dekrypterer ciphertext og konverterer resultatet tilbage til tekst
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


def encrypt_aes_cbc(plaintext):
    # Henter AES-nøglen
    key = get_aes_key()

    # Genererer en tilfældig IV på 16 bytes
    iv = os.urandom(16)

    # Laver padding så teksten passer til AES blokstørrelse
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    # Opretter AES-CBC cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Krypterer padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Samler IV og ciphertext og koder til base64-tekst
    token = base64.urlsafe_b64encode(iv + ciphertext).decode("utf-8")
    return token


def decrypt_aes_cbc(token):
    # Henter AES-nøglen
    key = get_aes_key()

    # Dekoder token fra base64 til bytes
    data = base64.urlsafe_b64decode(token.encode("utf-8"))

    # Splitter data i IV og ciphertext
    iv = data[:16]
    ciphertext = data[16:]

    # Opretter AES-CBC cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Dekrypterer ciphertext til padded plaintext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Fjerner padding og konverterer tilbage til tekst
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode("utf-8")


def encrypt_fernet(plaintext):
    # Opretter Fernet objekt med nøgle fra miljøvariabel
    f = Fernet(get_fernet_key())

    # Krypterer tekst og returnerer resultatet som streng
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_fernet(token):
    # Opretter Fernet objekt med nøgle fra miljøvariabel
    f = Fernet(get_fernet_key())

    # Dekrypterer token og returnerer resultatet som streng
    plaintext = f.decrypt(token.encode("utf-8"))
    return plaintext.decode("utf-8")


def encrypt_value(value, method=DEFAULT_METHOD):
    # Konverterer inputværdi til tekst før kryptering
    text = str(value)

    # Vælger krypteringsmetode ud fra parameteren method
    if method == "aes_gcm":
        return encrypt_aes_gcm(text)
    elif method == "aes_cbc":
        return encrypt_aes_cbc(text)
    elif method == "fernet":
        return encrypt_fernet(text)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")


def decrypt_value(value, method=DEFAULT_METHOD):
    # Vælger dekrypteringsmetode ud fra parameteren method
    if method == "aes_gcm":
        return decrypt_aes_gcm(value)
    elif method == "aes_cbc":
        return decrypt_aes_cbc(value)
    elif method == "fernet":
        return decrypt_fernet(value)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")


def encrypt_dataframe(df, method=DEFAULT_METHOD):
    # Laver en kopi af DataFrame så originalen ikke ændres
    encrypted_df = df.copy()

    # Krypterer alle værdier i hver kolonne
    for col in encrypted_df.columns:
        encrypted_df[col] = encrypted_df[col].apply(lambda x: encrypt_value(x, method))

    # Returnerer den krypterede DataFrame
    return encrypted_df


def decrypt_dataframe(df, method=DEFAULT_METHOD):
    # Laver en kopi af DataFrame så originalen ikke ændres
    decrypted_df = df.copy()

    # Dekrypterer alle værdier i hver kolonne
    for col in decrypted_df.columns:
        decrypted_df[col] = decrypted_df[col].apply(lambda x: decrypt_value(x, method))

    # Returnerer den dekrypterede DataFrame
    return decrypted_df


def cast_iris_columns(df):
    # Liste over de kolonner der skal være numeriske
    numeric_columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]

    # Konverterer de relevante kolonner fra tekst til numerisk datatype
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col])

    # Returnerer DataFrame med korrekt datatype på iris-målingerne
    return df