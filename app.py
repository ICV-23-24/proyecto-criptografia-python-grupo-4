from datetime import datetime
import os
from flask import Flask, render_template, request
import functions as f
from werkzeug.utils import secure_filename

app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        # Obtiene una lista de archivos enviados con el formulario
        archivos = request.files.getlist('archivo')
        # Obtiene el archivo seleccionado en el desplegable
        archivo2 = request.form.get('archivo')
        key_decrypt = request.form.get('key_decrypt')
        key = request.form.get('key')
        mode = request.form['mode']
        # Inicializa una variable donde están los archivos
        listado_archivos = []
        listado_claves = []
        # Determina el destino de los ficheros donde se guardarán los mensajes encriptados
        ruta = './archivos'
        rutaclaves = './claves'

        if mode == 'encrypt':
            # Seleccionamos el primer fichero
            docu = archivos[0]
            # Lee el contenido y lo guardo en una variable
            contenido = docu.read().decode('utf-8')
            # Recoge el nombre del fichero del formulario
            nuevo_nombre = request.form['archivo_nombre']
            # Añade una extensión a tu elección, por ejemplo ".txt"
            filename = secure_filename(nuevo_nombre + "_encriptado.txt")
            clave = f.generar_cadena()
            nombre_archivo = secure_filename(key + "_clave.txt")
            with open(os.path.join(rutaclaves, nombre_archivo), "w") as file2:
                file2.write(clave)
            # Crea una variable donde uso el contenido y la llave para encriptar el texto de la variable contenido
            encrypted_message = f.encrypt_message(contenido, clave)
            # Abre el archivo para escritura
            with open(os.path.join(ruta, filename), "w") as file:
                # Escribe el mensaje encriptado en el archivo
                file.write(encrypted_message)
            # Listamos los ficheros contenido en la ruta
            listado_archivos = f.listar(ruta)
            listado_claves = f.listarclaves(rutaclaves)
            return render_template('csimetrico.html',listado_claves=listado_claves, listado_archivos=listado_archivos,encrypted_message=encrypted_message,contenido=contenido, mode=mode)
        elif mode == 'decrypt':
            # Llamos a la función listar para obtener un listado de los archivos en la variable ruta
            listado_archivos = f.listar(ruta)
            # Obtiene el fichero seleccionado en el desplegable con su ruta completa
            ruta_completa = os.path.join(ruta, archivo2)
            # Obtiene el contenido del fichero que seleccionamos en el desplegable
            with open(ruta_completa, 'r') as file:
                contenido2 = file.read()
            # Ruta de destino para las claves
            rutaclaves = './claves'
            # Listamos el directorio con las claves
            listado_claves = f.listarclaves(rutaclaves)
            # Ruta con el fichero de la clave del desplegable
            ruta_completa2 = os.path.join(rutaclaves, key_decrypt)
            # Abrimos el fichero con la clave y leemos su contenido
            with open(ruta_completa2, 'r') as file2:
                contenidoclave = file2.read()
            # Finalmente desencriptamos el contenido del fichero seleccionado con la clave y el fichero elegidos
            decrypted_message = f.decrypt_message(contenido2, contenidoclave)
            return render_template('csimetrico.html', listado_claves=listado_claves, listado_archivos=listado_archivos,contenido2=contenido2,decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")

@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/otro/")
def otro():
    return render_template("otro.html")



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


if __name__ == '__main__':
    app.run(debug=True, port=5000)