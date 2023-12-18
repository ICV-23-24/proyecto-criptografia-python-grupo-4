import os
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import base64
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

encrypted_message = ""



#Script funcional 

# if __name__ == '__main__':
#     private_key, public_key = generate_key()

#     plaintext = 'Hola, Mundo'

#     ciphertext = encrypt(plaintext, public_key)

#     if ciphertext != "error":
#         decrypt_plaintext = decrypt(ciphertext, private_key)
#         if decrypt_plaintext != "error":
#             print("Plain Text = {0}".format(plaintext))
#             print("Texto Encriptado = {0}".format(ciphertext))
#             print("Texto Desencriptado = {0}".format(decrypt_plaintext))
#         else:
#             print("Ha ocurrido un error en la desencriptación")
#     else:
#         print("Ha ocurrido un error en la encriptación")


# Script sin comprobación de errores

# if __name__ == '__main__':
#     private_key, public_key = generate_key()

#     plaintext = 'Hola, Mundo'

#     ciphertext = encrypt(plaintext, public_key)
#     decrypt_plaintext = decrypt(ciphertext, private_key)

#     print("Plain Text = {0}".format(plaintext))
#     print("Texto Encriptado = {0}".format(ciphertext))
#     print("Texto Desencriptado = {0}".format(decrypt_plaintext))

