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

@app.route('/csimetrico', methods=['GET', 'POST'])
def csimetrico():
    if request.method == 'POST':
        archivos = request.files.getlist('archivo')
        archivo2 = request.form.get('archivo')
        key_decrypt = request.form.get('key_decrypt')
        key = request.form.get('key')
        mode = request.form['mode']
        listado_archivos = []
        listado_claves = []
        ruta = './archivos'
        rutaclaves = './claves'

        if mode == 'encrypt':
            docu = archivos[0]
            contenido = docu.read().decode('utf-8')
            nuevo_nombre = request.form['archivo_nombre']
            filename = secure_filename(nuevo_nombre + "_encriptado.txt")
            algoritmo = request.form['algoritmo']  # Nuevo campo para seleccionar el algoritmo

            if algoritmo not in ['AES', '3DES']:
                return render_template('csimetrico.html', error="Algoritmo no válido")

            clave = f.generar_cadena()  # Genera una clave aleatoria (puedes cambiarlo)
            nombre_archivo = secure_filename(key + "_clave.txt")
            with open(os.path.join(rutaclaves, nombre_archivo), "w") as file2:
                file2.write(clave)

            encrypted_message = f.encrypt_message(contenido, clave, algoritmo)
            with open(os.path.join(ruta, filename), "w") as file:
                file.write(encrypted_message)

            listado_archivos = f.listar(ruta)
            listado_claves = f.listarclaves(rutaclaves)
            return render_template('csimetrico.html', listado_claves=listado_claves, listado_archivos=listado_archivos,
                                   encrypted_message=encrypted_message, contenido=contenido, mode=mode)
        elif mode == 'decrypt':
            listado_archivos = f.listar(ruta)
            ruta_completa = os.path.join(ruta, archivo2)
            with open(ruta_completa, 'r') as file:
                contenido2 = file.read()

            rutaclaves = './claves'
            listado_claves = f.listarclaves(rutaclaves)
            ruta_completa2 = os.path.join(rutaclaves, key_decrypt)
            with open(ruta_completa2, 'r') as file2:
                contenidoclave = file2.read()

            decrypted_message = f.decrypt_message(contenido2, contenidoclave, algoritmo)
            return render_template('csimetrico.html', listado_claves=listado_claves, listado_archivos=listado_archivos,
                                   contenido2=contenido2, decrypted_message=decrypted_message, mode=mode)

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