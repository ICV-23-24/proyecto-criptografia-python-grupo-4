from datetime import datetime
from flask import Flask, render_template, request
import functions as f
import secrets
import string

app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    def generar_clave(longitud):
        caracteres = string.ascii_letters + string.digits
        clave_aleatoria = ''.join(secrets.choice(caracteres) for i in range(longitud))
        return clave_aleatoria

    longitud_clave = 12  # Cambia la longitud según tus necesidades
    key = None

    if request.method == 'POST':
        message = request.form['message']
        mode = request.form['mode']

        if mode == 'encrypt':
            key = generar_clave(longitud_clave)  # Genera la clave si se elige cifrar
            encrypted_message = f.encrypt_message(message, key)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, clave=key, mode=mode)

        elif mode == 'decrypt':
            if key is not None:
                decrypted_message = f.decrypt_message(message, key)
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