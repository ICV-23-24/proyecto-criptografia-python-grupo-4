from datetime import datetime
from flask import Flask, render_template, request
import functions as f
from pydrive2 import drive

app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']
        mode = request.form['mode']

        if mode == 'encrypt':
            encrypted_message = f.encrypt_message(message, key)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, mode=mode)
        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, key)
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")

@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")

@app.route("/chibrido/", methods=['GET','POST'])
def chibrido():
    if request.method == 'POST':
        filename = request.form['filename']
        key_symmetric = request.form['key_symmetric']
        key_public = request.form['key_public']

        # Cifrar el archivo
        ciphertext = f.encrypt_hybrid(filename, key_symmetric, key_public)

        # Subir el archivo cifrado a Google Drive
        drive.upload_file(ciphertext, filename)

        return render_template('chibrido.html', success=True)

    return render_template('chibrido.html')

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