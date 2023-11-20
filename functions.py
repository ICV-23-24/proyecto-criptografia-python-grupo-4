from random import sample
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

# def decrypt_message(message, key):
#     key = key.encode('utf-8')
#     cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
#     decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
#     return decrypted_message

def stringAleatorio():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio
