from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
from random import sample
from werkzeug.utils import secure_filename 
import os



def encrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

def decrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
    return decrypted_message

def stringAleatorio():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

def select_file(file,contenido):
    
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
     
    upload_path = os.path.join (basepath, './archivos', nuevoNombreFile) 
    file.save(upload_path)
    with open(upload_path, 'rb') as file:    
            contenido = file.read()

    # headers = {"Authorization": "Bearer ya29.a0AfB_byCPOWVfLBU571P9QS3p4RFx2xTpc1zZrKub1SiCKLLd5Tsu2kcBozgOtIK_yqJx7HilJW2Ombx0co9xLWIeE0PbyEY9dqW_DJU2pgYRZpAXy7zA63IrZJVGeVIPWceEG_v7PaZDs2pTi4Ld-VLhmH_R5rWZO9w0aCgYKAfQSARMSFQHGX2MiarGHG5c9yIAisph8KfDiGQ0171"}

    # nuevo_nombre_drive = stringAleatorio() + extension
    # para = {
    #         "name": nuevo_nombre_drive
    # }
    # files = {
    #     "data": ("metadata", json.dumps(para), "application/json; charset=UTF-8"),
    #     "file": (nuevo_nombre_drive, contenido)
    # }
    # r = requests.post(
    #     "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    #     headers=headers,
    #     files=files,
    # )


            