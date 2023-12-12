from Cryptodome.Cipher import AES,DES3
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
import os
from os.path import isfile, join
import string
import random
from smb.SMBConnection import SMBConnection
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


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

def conectar_samba():
    try:
        # Configura tus credenciales y detalles del servidor Samba aquí
        SMB_HOST = '192.168.8.142'
        SMB_PORT = 139
        SMB_USERNAME = 'pedro'
        SMB_PASSWORD = 'pedro'
        MY_NAME = 'samba'
        REMOTE_NAME = 'samba'

        # Establecer la conexión Samba
        smb_connection = SMBConnection(SMB_USERNAME, SMB_PASSWORD, MY_NAME, REMOTE_NAME, use_ntlm_v2=True)
        if smb_connection.connect(SMB_HOST, SMB_PORT):
            print("Conexión exitosa")
            return smb_connection
    except Exception as e:
        print(f"Error al conectar con Samba: {e}")
        return None


def cargar_samba(ruta_completa_aes, smb_connection):
        try:
            # Configura tus credenciales y detalles del servidor Samba aquí
            SMB_SHARE_FOLDER = 'python'

            # Obtén la ruta completa del archivo seleccionado
            ruta_local = os.path.join(ruta_completa_aes)

            if not os.path.exists(ruta_local):
                raise FileNotFoundError(f"El archivo local no existe: {ruta_local}")

                # Abre el archivo en modo binario ('rb')
            with open(ruta_local, 'rb') as file_content:
                # Almacena el archivo en Samba
                smb_connection.storeFile(SMB_SHARE_FOLDER, os.path.basename(ruta_local), file_content)

            # Cierra la conexión Samba después de realizar la operación

            return True  # Éxito
        except Exception as e:
            print(f"Error al cargar a Samba: {e}")
        return False

def listar_samba(smb_connection):
    try:
        # Configura tus credenciales y detalles del servidor Samba aquí
        SMB_SHARE_FOLDER = 'python'
        SMB_PATH = '/'

        # Lista los archivos en el directorio remoto
        files = smb_connection.listPath(SMB_SHARE_FOLDER, SMB_PATH)

        # Imprime los nombres de los archivos
        archivos_remotos = [file.filename for file in files]
        # print(archivos_remotos)
        return archivos_remotos
    except Exception as e:
        print(f"Error al listar archivos en Samba: {e}")
        return []
    
def descargar_samba(smb_connection,archivo_samba_seleccionado):
    try:
        ruta_local = './archivos'

        local_file_path = os.path.join(ruta_local, archivo_samba_seleccionado)
        
        with open(local_file_path, 'wb') as des:
            smb_connection.retrieveFile("python", archivo_samba_seleccionado, des)

        return local_file_path

    except Exception as e:
        print(f"Error al descargar el archivo desde Samba: {e}")
        return None

def descargar_sambaclave(smb_connection,clave_samba_seleccionado):
    try:
        ruta_local = './claves'

        local_file_path = os.path.join(ruta_local, clave_samba_seleccionado)
        
        with open(local_file_path, 'wb') as des:
            smb_connection.retrieveFile("python", clave_samba_seleccionado, des)

        return local_file_path

    except Exception as e:
        print(f"Error al descargar el archivo desde Samba: {e}")
        return None
    

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

