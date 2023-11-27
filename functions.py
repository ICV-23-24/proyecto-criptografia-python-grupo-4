from random import sample
import secrets
import string
from Cryptodome.Cipher import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(key, plaintext, output_filename):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=backend)
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(output_filename, 'wb') as encrypted_file:
        encrypted_file.write(ciphertext)

def decrypt_file(key, ciphertext, output_filename):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=backend)
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_filename, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

# def stringAleatorio():
#     #Generando string aleatorio
#     string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
#     longitud         = 20
#     secuencia        = string_aleatorio.upper()
#     resultado_aleatorio  = sample(secuencia, longitud)
#     string_aleatorio     = "".join(resultado_aleatorio)
#     return string_aleatorio

def save_key_to_file(file_key, key_filename):
    with open(key_filename, 'wb') as key_file:
        key_file.write(file_key)

def read_key_from_file(key_filename):
    with open(key_filename, 'rb') as key_file:
        return key_file.read()
