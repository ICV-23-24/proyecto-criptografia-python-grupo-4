from datetime import datetime
from random import sample
import functions as f
import secrets
import string
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename 
import os


app = Flask(__name__)
app.secret_key = '1234'

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

def generar_clave(longitud):
    caracteres = string.ascii_letters + string.digits
    clave_aleatoria = ''.join(secrets.choice(caracteres) for i in range(longitud))
    return clave_aleatoria

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    if 'key' not in session:
        session['key'] = generar_clave(12)

    if request.method == 'POST':
        message = request.form['message']
        mode = request.form['mode']
        # file     = request.files['archivo']
        # basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
        # filename = secure_filename(file.filename) #Nombre original del archivo

        # extension           = os.path.splitext(filename)[1]
        # nuevoNombreFile     = f.stringAleatorio() + extension
     
        # upload_path = os.path.join (basepath, './archivos', nuevoNombreFile) 
        # file.save(upload_path)

        if mode == 'encrypt':
            encrypted_message = f.encrypt_message(message, session['key'])
            return render_template('csimetrico.html', encrypted_message=encrypted_message, clave=session['key'], mode=mode)

        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, session['key'])
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

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