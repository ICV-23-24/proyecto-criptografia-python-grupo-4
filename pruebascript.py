import os
from Crypto.Cipher import RC5

def cifrar(archivo_a_cifrar, archivo_clave):
    # Generamos una clave aleatoria de 128 bits
    clave = os.urandom(128)

    # Guardamos la clave en un archivo
    with open(archivo_clave, "wb") as f:
        f.write(clave)

    # Creamos un objeto de cifrado RC5
    cipher = RC5.new(clave, RC5.MODE_ECB)

    # Leemos el archivo a cifrar
    with open(archivo_a_cifrar, "rb") as f:
        datos_a_cifrar = f.read()

    # Ciframos los datos
    datos_cifrados = cipher.encrypt(datos_a_cifrar)

    # Guardamos los datos cifrados en un nuevo archivo
    with open(archivo_a_cifrar + ".cifrado", "wb") as f:
        f.write(datos_cifrados)

def descifrar(archivo_cifrado, archivo_clave):
    # Leemos la clave
    with open(archivo_clave, "rb") as f:
        clave = f.read()

    # Creamos un objeto de cifrado RC5
    cipher = RC5.new(clave, RC5.MODE_ECB)

    # Leemos el archivo cifrado
    with open(archivo_cifrado, "rb") as f:
        datos_cifrados = f.read()

    # Desciframos los datos
    datos_descifrados = cipher.decrypt(datos_cifrados)

    # Guardamos los datos descifrados en un nuevo archivo
    with open(archivo_cifrado[:-8], "wb") as f:
        f.write(datos_descifrados)

if __name__ == "__main__":
    # Fichero a cifrar
    archivo_a_cifrar = "archivo.txt"

    # Fichero donde se guardará la clave
    archivo_clave = "clave.txt"

    # Ciframos el archivo
    cifrar(archivo_a_cifrar, archivo_clave)

    # Desciframos el archivo
    descifrar(archivo_a_cifrar + ".cifrado", archivo_clave)