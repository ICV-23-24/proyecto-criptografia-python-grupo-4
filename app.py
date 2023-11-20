from datetime import datetime
from flask import Flask, render_template, request
import functions as f
import asimetric as x
import os
from werkzeug.utils import secure_filename 
import json
import requests

app = Flask(__name__)


# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        contenido = ""
        message = request.form['message']
        key = request.form['key']
        mode = request.form['mode']
        file     = request.files['archivo']
        basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename) #Nombre original del archivo

        extension           = os.path.splitext(filename)[1]
        nuevoNombreFile     = f.stringAleatorio() + extension
     
        upload_path = os.path.join (basepath, './archivos', nuevoNombreFile) 
        file.save(upload_path)
        with open(upload_path, 'rb') as file:    
                contenido = file.read()

        headers = {"Authorization": "Bearer ya29.a0AfB_byCPOWVfLBU571P9QS3p4RFx2xTpc1zZrKub1SiCKLLd5Tsu2kcBozgOtIK_yqJx7HilJW2Ombx0co9xLWIeE0PbyEY9dqW_DJU2pgYRZpAXy7zA63IrZJVGeVIPWceEG_v7PaZDs2pTi4Ld-VLhmH_R5rWZO9w0aCgYKAfQSARMSFQHGX2MiarGHG5c9yIAisph8KfDiGQ0171"}

        nuevo_nombre_drive = f.stringAleatorio() + extension
        para = {
                "name": nuevo_nombre_drive
        }
        files = {
            "data": ("metadata", json.dumps(para), "application/json; charset=UTF-8"),
            "file": (nuevo_nombre_drive, contenido)
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files,
        )

        if mode == 'encrypt':
            encrypted_message = f.encrypt_message(message, key)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, mode=mode)
        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, key)
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")

@app.route("/casimetrico/", methods=['GET','POST'])
def casimetrico():

    global encrypted_message

    if request.method == 'POST':
        message = request.form['message']
        private_key, public_key = x.generate_key()
        print("Public Key:", public_key)
        print("Private Key:", private_key)
        # key = request.form['key']
        mode = request.form['mode']

        if mode == 'encrypt':
            encrypted_message = x.encrypt(message, public_key)
            return render_template('casimetrico.html', encrypted_message=encrypted_message, mode=mode)
        elif mode == 'decrypt':
            decrypted_message = x.decrypt(encrypted_message, private_key)
            return render_template('casimetrico.html', decrypted_message=decrypted_message, mode=mode)


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
    app.run(debug=True, port=3000)
