from Cryptodome.Cipher import AES,DES3
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
import os
from os.path import isfile, join
import string
import random

# def encrypt_message(contenido, clave):
#     key = clave.encode('utf-8')
#     cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
#     encrypted_message = cipher.encrypt(pad(contenido.encode('utf-8'), AES.block_size))
#     return b64encode(encrypted_message).decode('utf-8')

# def decrypt_message(contenido2, contenidoclave):
#     key = contenidoclave.encode('utf-8')
#     cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
#     decrypted_message = unpad(cipher.decrypt(b64decode(contenido2)), AES.block_size).decode('utf-8')
#     return decrypted_message

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

# def encrypt_message_3des(contenido, clave):
#     # Asegúrate de que la clave tenga una longitud válida para 3DES (16, 24 o 32 bytes)
#     key = clave.encode('utf-8')[:24]

#     # Crea un objeto de cifrado 3DES en modo ECB
#     cipher = DES3.new(key, DES3.MODE_ECB)

#     # Aplica el relleno al contenido y cifra el mensaje
#     encrypted_message = cipher.encrypt(pad(contenido.encode('utf-8'), DES3.block_size))

#     # Codifica el mensaje cifrado en base64 y devuelve el resultado como una cadena
#     return b64encode(encrypted_message).decode('utf-8')

# def decrypt_message_3des(contenido, contenidoclave):
#     # Asegúrate de que la clave tenga una longitud válida para 3DES (16, 24 o 32 bytes)
#     key = contenidoclave.encode('utf-8')[:24]

#     # Crea un objeto de cifrado 3DES en modo ECB
#     cipher = DES3.new(key, DES3.MODE_ECB)

#     # Descodifica el mensaje cifrado en base64 y luego descifra el mensaje
#     decrypted_message = unpad(cipher.decrypt(b64decode(contenido)), DES3.block_size).decode('utf-8')

#     # Devuelve el mensaje descifrado
#     return decrypted_message

def encrypt_message(contenido, clave, algoritmo):
    if algoritmo == 'AES':
        cipher = AES.new(pad(clave.encode('utf-8'), AES.block_size), AES.MODE_ECB)
    elif algoritmo == '3DES':
        clave = clave.encode('utf-8')[:24]  # Asegurar que la clave tenga longitud válida para 3DES
        cipher = DES3.new(clave, DES3.MODE_ECB)
    else:
        raise ValueError("Algoritmo de cifrado no válido")

    encrypted_message = cipher.encrypt(pad(contenido.encode('utf-8'), max(AES.block_size, DES3.block_size)))
    return b64encode(encrypted_message).decode('utf-8')

# Función para desencriptar un mensaje usando AES o 3DES
def decrypt_message(contenido, contenidoclave, algoritmo):
    if algoritmo == 'AES':
        cipher = AES.new(pad(contenidoclave.encode('utf-8'), AES.block_size), AES.MODE_ECB)
    elif algoritmo == '3DES':
        contenidoclave = contenidoclave.encode('utf-8')[:24]  # Asegurar que la clave tenga longitud válida para 3DES
        cipher = DES3.new(contenidoclave, DES3.MODE_ECB)
    else:
        raise ValueError("Algoritmo de cifrado no válido")

    decrypted_message = unpad(cipher.decrypt(b64decode(contenido)), max(AES.block_size, DES3.block_size)).decode('utf-8')
    return decrypted_message