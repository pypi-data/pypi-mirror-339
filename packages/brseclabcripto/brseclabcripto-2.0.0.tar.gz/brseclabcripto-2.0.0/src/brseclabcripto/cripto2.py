'''
Functions for AES256-GCM encryption/decryption (pyca/cryptography and gpg) and Argon2 hashing.
This module provides functions to generate an AES key, encrypt and decrypt messages,
and hash and verify passwords using Argon2.
It uses the PyCryptodome library for AES encryption and Argon2 for password hashing.
It is important to note that the AES key should be kept secret and secure.
The Argon2 hash should also be stored securely, as it is used to verify passwords.
This module is intended for educational purposes and should not be used in 
production without proper security measures.

Author: RAFAEL PERAZZO B MOTA
Date: 2025-03-30
Version: 1.1
'''
import base64
import secrets
import cryptography
import gnupg
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import argon2
from argon2 import PasswordHasher

def aes_gcm_encrypt(key, plaintext):
    '''
    Encrypts the plaintext using AES GCM encryption with a random nonce.
    :param key: AES key (must be 16, 24, or 32 bytes long) - bytes
    :param plaintext: plaintext to be encrypted - bytes
    :return: ciphertext (nonce + ciphertext + tag) - base64 string
    '''
    if isinstance(key, str):
        # Convert hexadecimal string key to bytes
        key = bytes.fromhex(key)
    if isinstance(plaintext, str):
        # Convert string plaintext to bytes
        plaintext = plaintext.encode()
    cipher = AESGCM(key)
    nonce = secrets.token_bytes(12)  # Generate a random nonce
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def aes_gcm_decrypt(key, ciphertext):
    '''
    Decrypts the ciphertext using AES GCM decryption.
    :param key: AES key (must be 16, 24, or 32 bytes long) - bytes
    :param ciphertext: ciphertext to be decrypted (nonce + ciphertext + tag) 
    - bytes or base64 string
    :return: decrypted plaintext - string
    '''
    if isinstance(key, str):
        # Convert hexadecimal string key to bytes
        key = bytes.fromhex(key)
    if isinstance(ciphertext, str):
        # Convert base64 string ciphertext to bytes
        ciphertext = base64.b64decode(ciphertext)
    nonce = ciphertext[:12]
    ciphertext = ciphertext[12:]
    cipher = AESGCM(key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')

def gpg_encrypt(key, plaintext):
    '''
    Encrypts the plaintext using GPG Symmetric encryption.
    :param key: GPG passphrase - string
    :param plaintext: plaintext to be encrypted - string
    :return: ciphertext - string
    '''
    gpg = gnupg.GPG()
    # Encrypt the plaintext
    encrypted_data = gpg.encrypt(plaintext, passphrase=key, symmetric='AES256', recipients=None)
    return str(encrypted_data)

def gpg_decrypt(key, ciphertext):
    '''
    Decrypts the ciphertext using GPG Symmetric decryption.
    :param key: GPG passphrase - string
    :param ciphertext: ciphertext to be decrypted - string
    :return: decrypted plaintext - string
    '''
    gpg = gnupg.GPG()
    # Decrypt the ciphertext
    decrypted_data = gpg.decrypt(ciphertext,passphrase=key)
    return str(decrypted_data)

def hash_hmac(key, message):
    '''
    Computes the HMAC of the given message using the provided key.
    :param key: HMAC key - bytes
    :param message: message to be hashed - bytes
    :return: HMAC - hexadecimal string
    '''
    if isinstance(key, str):
        # Convert hexadecimal string key to bytes
        key = bytes.fromhex(key)
    if isinstance(message, str):
        # Convert string message to bytes
        message = message.encode()
    h = hmac.HMAC(key, hashes.SHA3_256())
    h.update(message)
    return h.finalize().hex()

def hash_hmac_verify(key, message, hmac_value):
    '''
    Verifies the HMAC of the given message using the provided key.
    :param key: HMAC key - bytes or hexadecimal string
    :param message: message to be hashed - bytes or string
    :param hmac_value: HMAC to be verified - bytes or hexadecimal string
    :return: True if the HMAC is valid, False otherwise
    '''

    if isinstance(key, str):
        # Convert hexadecimal string key to bytes
        key = bytes.fromhex(key)
    if isinstance(message, str):
        # Convert string message to bytes
        message = message.encode()
    if isinstance(hmac_value, str):
        # Convert hexadecimal string HMAC to bytes
        try:
            hmac_value = bytes.fromhex(hmac_value)
        except ValueError:
            # If the HMAC is not a valid hexadecimal string, return False
            return False
    h = hmac.HMAC(key, hashes.SHA3_256())
    h.update(message)
    try:
        h.verify(hmac_value)
        return True
    except cryptography.exceptions.InvalidSignature:
        return False

def hash_argon2id(key, password):
    '''
    Applies Argon2 hashing to the password using a HMAC.
    :param key: key for the HMAC - bytes or hexadecimal string
    :param password: password to be hashed - string
    :return: Argon2 hash - string
    '''
    if isinstance(key, str):
        # Convert hexadecimal string key to bytes
        key = bytes.fromhex(key)
    if isinstance(password, str):
        # Convert string password to bytes
        password = password.encode()
    # Create the HMAC
    signature = hash_hmac(key, password)
    # Apply Argon2 hashing
    ph = PasswordHasher(time_cost=3, memory_cost=65536, 
                        parallelism=4, hash_len=32, salt_len=16, encoding='utf-8')
    hash_argon = ph.hash(signature)
    return hash_argon

def hash_argon2id_verify(hash_argon, key, password):
    '''
    Verifies if the Argon2 hash matches the password.
    :param hash_argon: stored Argon2 hash - string
    :param key: key for the HMAC - bytes or hexadecimal string
    :param password: password to be verified - string
    :return: True if the password is correct, False otherwise
    '''
    if isinstance(key, str):
        # Convert hexadecimal string key to bytes
        key = bytes.fromhex(key)
    if isinstance(password, str):
        # Convert string password to bytes
        password = password.encode()
    # Create the HMAC
    signature = hash_hmac(key, password)
    # Apply Argon2 hashing
    ph = PasswordHasher(time_cost=3, memory_cost=65536, 
                        parallelism=4, hash_len=32, salt_len=16, encoding='utf-8')
    try:
        ph.verify(hash_argon, signature)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False

