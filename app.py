from datetime import datetime
from random import sample
import functions as f
# import secrets
# import string
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename 
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    if request.method == 'POST':
        file = request.files['archivo']
        basepath = os.path.dirname(__file__)
        filename = secure_filename(file.filename)

        extension = os.path.splitext(filename)[1]
        nuevoNombreFile = f.stringAleatorio() + extension

        upload_path = os.path.join(basepath, 'archivos', nuevoNombreFile)
        file.save(upload_path)

        key = os.urandom(32)  # Clave de 256 bits para AES

        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)

        with open(upload_path, 'rb') as original_file:
            original = original_file.read()

        f.encrypt_file(key, original, upload_path + '.enc.csv')

        session['key'] = key

        return render_template('csimetrico.html', encrypted_file=upload_path + '.enc.csv', clave=key, mode='encrypt')

        # elif mode == 'decrypt':
        #     decrypted_message = f.decrypt_message(message, session['key'])
        #     return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

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