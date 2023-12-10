from Cryptodome.Cipher import AES,DES3
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
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
        if len(clave) != 16:
            raise ValueError("La clave para AES debe ser de 16 bytes")
        cipher = AES.new(clave.encode('utf-8'), AES.MODE_ECB)
    elif algoritmo == '3DES':
        if len(clave) < 24:
            clave = clave.ljust(24, '\0')
        elif len(clave) > 24:
            clave = clave[:24]
        if len(clave) != 24:
            raise ValueError("La clave para 3DES debe ser de 24 bytes")
        cipher = DES3.new(clave.encode('utf-8'), DES3.MODE_ECB)
    else:
        raise ValueError("Algoritmo de cifrado no válido")

    encrypted_message = cipher.encrypt(pad(contenido.encode('utf-8'), max(AES.block_size, DES3.block_size)))
    return b64encode(encrypted_message).decode('utf-8')

# Función para desencriptar un mensaje usando AES o 3DES
def decrypt_message(contenido, contenidoclave, algoritmo, ruta_completa):
    if algoritmo == 'AES':
        if len(contenidoclave) != 16:
            raise ValueError("La clave para AES debe ser de 16 bytes")
        cipher = AES.new(contenidoclave.encode('utf-8'), AES.MODE_ECB)
    elif algoritmo == '3DES':
        if len(contenidoclave) != 24:
            raise ValueError("La clave para 3DES debe ser de 24 bytes")
        cipher = DES3.new(contenidoclave.encode('utf-8'), DES3.MODE_ECB)
    else:
        raise ValueError("Algoritmo de cifrado no válido")

    decrypted_message = unpad(cipher.decrypt(b64decode(contenido)), max(AES.block_size, DES3.block_size)).decode('utf-8')

    # Sobrescribe el archivo original con el mensaje desencriptado
    with open(ruta_completa, 'w') as file:
        file.write(decrypted_message)

    return decrypted_message

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def export_private_key(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

def export_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def import_public_key(public_key_bytes):
    return serialization.load_pem_public_key(public_key_bytes, backend=default_backend())

def encrypt_message(public_key, message):
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def decrypt_message(private_key, encrypted_message):
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message

def import_private_key(private_key_bytes):
    return serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )

def import_public_key(public_key_pem):
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )
    return public_key

def encrypt_file(public_key, file):
    # Lee el contenido del archivo
    file_content = file.read()
    # Encripta el contenido del archivo
    encrypted_file_content = public_key.encrypt(
        file_content,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_file_content

def import_private_key(private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )
    return private_key

def decrypt_file(private_key, encrypted_file):
    encrypted_data = encrypted_file.read()
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data