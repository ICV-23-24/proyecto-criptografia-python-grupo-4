from datetime import datetime
from random import sample
import functions as f
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename 
import os
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = b'1234'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    archivos_en_carpeta = os.listdir('./archivos')
    claves = [filename for filename in archivos_en_carpeta if filename.endswith('.key')]
    print("Claves:", claves)
        
    archivo_seleccionado = None
    mode = None  # Define the 'mode' variable

    if request.method == 'POST':
        print("Form data received:", request.form)
        archivo_seleccionado = request.form.get('archivo')
        file = request.files['archivo']
        basepath = os.path.dirname(__file__)
        filename = secure_filename(file.filename)

        upload_path = os.path.join(basepath, 'archivos', filename)
        file.save(upload_path)

        key_filename = os.path.join(basepath, 'claves', f'{filename}.key')

        file_key = os.urandom(32)

        with open(upload_path, 'rb') as original_file:
            original = original_file.read()

        mode = request.form.get('mode')
        claves = [filename for filename in os.listdir('./claves') if filename.endswith('.key')]
        print("Claves after form submission:", claves)

        if mode == 'encrypt':
            f.encrypt_file(file_key, original, upload_path + '.enc.csv')
            f.save_key_to_file(file_key, key_filename)
            return render_template('csimetrico.html', encrypted_file=upload_path + '.enc.csv', clave=file_key, archivos=archivos_en_carpeta, archivo_seleccionado=archivo_seleccionado, mode=mode, claves=claves)

        elif mode == 'decrypt':
            decrypted_file_path = upload_path.replace('.enc.csv', '_decrypted.csv')
            f.decrypt_file(file_key, original, decrypted_file_path)
            file_key = f.read_key_from_file(key_filename)
            return render_template('csimetrico.html', decrypted_file=decrypted_file_path, archivo_seleccionado=archivo_seleccionado, mode=mode, claves=claves)

    return render_template("csimetrico.html", claves=claves)

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