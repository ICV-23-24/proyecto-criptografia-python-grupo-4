from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
import os
from os.path import isfile, join
import string
import random

def encrypt_message(contenido, clave):
    key = clave.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(contenido.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

def decrypt_message(contenido2, contenidoclave):
    key = contenidoclave.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(contenido2)), AES.block_size).decode('utf-8')
    return decrypted_message

# Función para listar solo ficheros con el argumento ruta que pasa la carpeta a listar
def listar(ruta):
    archivos = [a for a in os.listdir(ruta) if isfile(join(ruta, a))]
    return archivos

def listarclaves(rutaclaves):
    keys = [a for a in os.listdir(rutaclaves) if isfile(join(rutaclaves, a))]
    return keys

# Generar una cadena de caracteres aleatoria
def generar_cadena(longitud=16):
    # Genera una cadena aleatoria usando letras y números
    caracteres = string.ascii_letters + string.digits
    cadena_aleatoria = ''.join(random.choice(caracteres) for _ in range(longitud))

    return cadena_aleatoria
