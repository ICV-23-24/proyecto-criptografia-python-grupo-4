from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for
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
        algoritmo = request.form['algoritmo']
        listado_archivos = []
        listado_claves = []
        ruta = './archivos'
        rutaclaves = './claves'

        if mode == 'encrypt':
            docu = archivos[0]
            contenido = docu.read().decode('utf-8')
            nuevo_nombre = request.form['archivo_nombre']
            filename = secure_filename(nuevo_nombre + "_encriptado.txt")

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
            if algoritmo == '3DES' and len(contenidoclave) != 24:
                return render_template('csimetrico.html', error="La clave para 3DES debe ser de 24 bytes")
        decrypted_message = f.decrypt_message(contenido2, contenidoclave, algoritmo, ruta_completa)
        return render_template('csimetrico.html', listado_claves=listado_claves, listado_archivos=listado_archivos,
                                   contenido2=contenido2, decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")

@app.route('/casimetrico', methods=['GET', 'POST'])
def casimetrico():
    encrypted_file_name = None
    decrypted_file_name = None
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'generate_keys':
            private_key, public_key = f.generate_keys()
            with open(os.path.join('claves', 'private_key.pem'), 'wb') as private_key_file:
                private_key_file.write(f.export_private_key(private_key))
            with open(os.path.join('claves', 'public_key.pem'), 'wb') as public_key_file:
                public_key_file.write(f.export_public_key(public_key))
        elif operation == 'import_key':
            public_key_file = request.files["public_key"]
            public_key = f.import_public_key(public_key_file.read())
            with open(os.path.join('claves', 'imported_public_key.pem'), 'wb') as imported_public_key_file:
                imported_public_key_file.write(f.export_public_key(public_key))
            return "Clave pública importada con éxito"
        elif operation == 'export_key':
            with open(os.path.join('claves', 'public_key.pem'), 'rb') as public_key_file:
                public_key = f.import_public_key(public_key_file.read())
            response = make_response(f.export_public_key(public_key))
            response.headers.set('Content-Type', 'application/octet-stream')
            response.headers.set('Content-Disposition', 'attachment', filename='public_key.pem')
            return response
        elif operation == 'encrypt_message':
            message = request.form["message"].encode('utf-8')
            with open(os.path.join('claves', 'public_key.pem'), 'rb') as public_key_file:
                public_key = f.import_public_key(public_key_file.read())
            encrypted_message = f.encrypt_message(public_key, message)
            return jsonify({"encrypted_message": base64.b64encode(encrypted_message).decode('utf-8')})
        elif operation == 'decrypt_message':
            encrypted_message = base64.b64decode(request.form["encrypted_message"])
            with open(os.path.join('claves', 'private_key.pem'), 'rb') as private_key_file:
                private_key = f.import_private_key(private_key_file.read())
            original_message = f.decrypt_message(private_key, encrypted_message)
            return jsonify({"original_message": original_message.decode('utf-8')})
        elif operation == 'encrypt_file':
            if 'file' not in request.files:
                return "No se subió ningún archivo", 400
            file = request.files['file']
            with open(os.path.join('claves', 'public_key.pem'), 'rb') as public_key_file:
                public_key = f.import_public_key(public_key_file.read())
            encrypted_file = f.encrypt_file(public_key, file)
            encrypted_file_name = file.filename
            with open(os.path.join('archivos', file.filename), 'wb') as encrypted_file_file:
                encrypted_file_file.write(encrypted_file)
        elif operation == 'decrypt_file':
            if 'file' not in request.form:
                return "No se seleccionó ningún archivo", 400
            file_name = request.form['file']
            if 'key' not in request.form:
                return "No se seleccionó ninguna clave", 400
            key_name = request.form['key']
            with open(os.path.join('claves', key_name), 'rb') as private_key_file:
                private_key = f.import_private_key(private_key_file.read())
            with open(os.path.join('archivos', file_name), 'rb') as file:
                decrypted_file = f.decrypt_file(private_key, file)
            decrypted_file_name = 'decrypted_' + file_name
            with open(os.path.join('archivos', decrypted_file_name), 'wb') as decrypted_file_file:
                decrypted_file_file.write(decrypted_file)
    keys = os.listdir('claves')
    files = os.listdir('archivos')
    return render_template("casimetrico.html", keys=keys, files=files, decrypted_file_name=decrypted_file_name, encrypted_file_name=encrypted_file_name)

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