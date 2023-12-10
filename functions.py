from Cryptodome.Cipher import AES,DES3,PKCS1_OAEP
from Cryptodome.Util.Padding import pad,unpad
from Cryptodome.PublicKey import RSA
from base64 import b64encode, b64decode
import os
from os.path import isfile, join
import string
import random
import base64

# Funciones simétricas

def encrypt_message_AES(contenido, clave):
    key = clave.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message_AES = cipher.encrypt(pad(contenido.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message_AES).decode('utf-8')

def decrypt_message_AES(contenido2, contenidoclave):
    key = contenidoclave.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message_AES = unpad(cipher.decrypt(b64decode(contenido2)), AES.block_size).decode('utf-8')
    return decrypted_message_AES

def encrypt_message_3DES(contenido, clave):
    key = clave.encode('utf-8')[:24]
    cipher = DES3.new(key, DES3.MODE_ECB)
    encrypted_message_3DES = cipher.encrypt(pad(contenido.encode('utf-8'), DES3.block_size))
    return b64encode(encrypted_message_3DES).decode('utf-8')

def decrypt_message_3des(contenido, contenidoclave):
    key = contenidoclave.encode('utf-8')[:24]
    cipher = DES3.new(key, DES3.MODE_ECB)
    decrypted_message_3DES = unpad(cipher.decrypt(b64decode(contenido)), DES3.block_size).decode('utf-8')
    return decrypted_message_3DES

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

#################################################################################################

# Funciones asimetricas

# Generar las claves
rutaclaves_asimetrico = './clavesasimetrico'

def generate_key():
    key = RSA.generate(2048)
    private_key = key.export_key().decode('utf-8')
    public_key = key.publickey().export_key().decode('utf-8')
    return private_key, public_key

def generate_and_save_keys():
    private_key, public_key = generate_key()
    
    private_key_path = os.path.join(rutaclaves_asimetrico, "private_key.txt")
    public_key_path = os.path.join(rutaclaves_asimetrico, "public_key.txt")

    # Guardar las claves en archivos
    with open(private_key_path, "w") as private_key_file:
        private_key_file.write(private_key)

    with open(public_key_path, "w") as public_key_file:
        public_key_file.write(public_key)

# Encriptar el mensaje
def encrypt(message: str, public_key: str) -> str:
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message.encode('utf-8'))
    return base64.b64encode(ciphertext).decode('utf8')

# Desencriptar el mensaje
def decrypt(ciphertext: str, private_key: str) -> str:
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    message = cipher.decrypt(ciphertext)
    
    return message.decode('utf-8')

def listarclavesasimetricas(rutaclaves_asimetrico):
    keys = [a for a in os.listdir(rutaclaves_asimetrico) if isfile(join(rutaclaves_asimetrico, a))]
    return keys

