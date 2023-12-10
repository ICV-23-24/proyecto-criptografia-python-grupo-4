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
    smb_connection = f.conectar_samba()
    ruta = './archivos'
    rutaclaves = './claves'
    listado_samba = f.listar_samba(smb_connection)
    listado_archivos_aes = f.listar(ruta)
    listado_claves = f.listarclaves(rutaclaves)
    listado_archivos_3des = f.listar(ruta)
    archivo2_aes = request.form.get('archivo_aes')

    if request.method == 'POST':
        contenido_aes = ""
        contenido_3des = ""
        ruta_completa_aes = ""
        # Obtiene una lista de archivos enviados con el formulario de AES
        archivos_aes = request.files.getlist('archivo_aes')
        # Obtiene una lista de archivos enviados con el formulario de 3DES
        archivos_3des = request.files.getlist('archivo_3des')
        archivos_samba = request.files.getlist('archivo_samba')

        
        # Obtiene el archivo seleccionado en el desplegable del formulario de AES
        archivo2_aes = request.form.get('archivo_aes')
        # Obtiene el archivo seleccionado en el desplegable del formulario de 3DES
        archivo2_3des = request.form.get('archivo_3des')

        key_decrypt_aes = request.form.get('key_decrypt_aes')
        key_decrypt_3des = request.form.get('key_decrypt_3des')

        key_aes = request.form.get('key_aes')
        key_3des = request.form.get('key_3des')

        mode_aes = request.form.get('mode_aes')
        mode_3des = request.form.get('mode_3des')

        mode_samba = request.form.get('descargar_samba')
        

       
        if mode_aes == 'encrypt_aes':
            # Seleccionamos el primer fichero para AES
            docu_aes = archivos_aes[0]
            # Lee el contenido y lo guarda en una variable
            contenido_aes = docu_aes.read().decode('utf-8')
            # Recoge el nombre del fichero del formulario
            nuevo_nombre_aes = request.form['archivo_nombre_aes']
            # Añade una extensión a tu elección, por ejemplo ".txt"
            filename_aes = secure_filename(nuevo_nombre_aes + "_encriptadoAES.txt")
            clave_aes = f.generar_cadena()
            nombre_archivo_aes = secure_filename(key_aes + "_clave_AES.txt")

            with open(os.path.join(rutaclaves, nombre_archivo_aes), "w") as file_aes:
                file_aes.write(clave_aes)

            # Abre el archivo para escritura
            with open(os.path.join(ruta, filename_aes), "w") as file_aes:
                file_aes.write(f.encrypt_message_AES(contenido_aes, clave_aes))
            
            listado_archivos_aes = f.listar(ruta)
            listado_claves = f.listarclaves(rutaclaves)
            listado_samba = f.listar_samba(smb_connection)

            
            return render_template('csimetrico.html', 
                                   listado_samba=listado_samba, 
                                   listado_claves=listado_claves, 
                                   listado_archivos_aes=listado_archivos_aes, 
                                   contenido_aes=contenido_aes, 
                                   listado_archivos_3des=listado_archivos_3des, 
                                   contenido_3des=contenido_3des, 
                                   mode_aes=mode_aes, 
                                   mode_3des=mode_3des)

        elif mode_3des == 'encrypt_3des':
            # Seleccionamos el primer fichero para 3DES
            docu_3des = archivos_3des[0]
            # Lee el contenido y lo guarda en una variable
            contenido_3des = docu_3des.read().decode('utf-8')
            # Recoge el nombre del fichero del formulario
            nuevo_nombre_3des = request.form['archivo_nombre_3des']
            # Añade una extensión a tu elección, por ejemplo ".txt"
            filename_3des = secure_filename(nuevo_nombre_3des + "_encriptado_3des.txt")
            clave_3des = f.generar_cadena()
            nombre_archivo_3des = secure_filename(key_3des + "_clave_3des.txt")

            with open(os.path.join(rutaclaves, nombre_archivo_3des), "w") as file_3des:
                file_3des.write(clave_3des)

            # Abre el archivo para escritura
            with open(os.path.join(ruta, filename_3des), "w") as file_3des:
                file_3des.write(f.encrypt_message_3DES(contenido_3des, clave_3des))

            # Listamos los ficheros contenidos en la ruta para 3DES
            listado_archivos_3des = f.listar(ruta)
            listado_claves = f.listarclaves(rutaclaves)
            listado_samba = f.listar_samba(smb_connection)

            return render_template('csimetrico.html', 
                                   listado_samba=listado_samba, 
                                   listado_claves=listado_claves, 
                                   listado_archivos_aes=listado_archivos_aes, 
                                   contenido_aes=contenido_aes, 
                                   listado_archivos_3des=listado_archivos_3des, 
                                   contenido_3des=contenido_3des, 
                                   mode_aes=mode_aes, 
                                   mode_3des=mode_3des)

        elif mode_aes == 'decrypt_aes':
            # Llamamos a la función listar para obtener un listado de los archivos en la variable ruta
            listado_archivos_aes = f.listar(ruta)
            # Obtiene el fichero seleccionado en el desplegable con su ruta completa
            ruta_completa_aes = os.path.join(ruta, archivo2_aes)
            # Obtiene el contenido del fichero que seleccionamos en el desplegable
            with open(ruta_completa_aes, 'r') as file_aes:
                contenido2_aes = file_aes.read()
            # Ruta de destino para las claves
            rutaclaves = './claves'
            # Listamos el directorio con las claves
            listado_claves = f.listarclaves(rutaclaves)
            # Ruta con el fichero de la clave del desplegable
            ruta_completa2_aes = os.path.join(rutaclaves, key_decrypt_aes)
            # Abrimos el fichero con la clave y leemos su contenido
            with open(ruta_completa2_aes, 'r') as file2_aes:
                contenidoclave_aes = file2_aes.read()
            # Finalmente desencriptamos el contenido del fichero seleccionado con la clave y el fichero elegidos
            decrypted_message_aes = f.decrypt_message_AES(contenido2_aes, contenidoclave_aes)
            print("Listado de archivos AES:", listado_archivos_aes)
            return render_template('csimetrico.html', 
                                   listado_samba=listado_samba, 
                                   listado_claves=listado_claves, 
                                   listado_archivos_aes=listado_archivos_aes, 
                                   contenido_aes=contenido_aes, 
                                   listado_archivos_3des=listado_archivos_3des, 
                                   contenido_3des=contenido_3des, 
                                   decrypted_message_aes=decrypted_message_aes, 
                                   mode_aes=mode_aes, 
                                   mode_3des=mode_3des)

        elif mode_3des == 'decrypt_3des':
            # Llamamos a la función listar para obtener un listado de los archivos en la variable ruta
            listado_archivos_3des = f.listar(ruta)
            # Obtiene el fichero seleccionado en el desplegable con su ruta completa
            ruta_completa_3des = os.path.join(ruta, archivo2_3des)
            # Obtiene el contenido del fichero que seleccionamos en el desplegable
            with open(ruta_completa_3des, 'r') as file_3des:
                contenido2_3des = file_3des.read()
            # Ruta con el fichero de la clave del desplegable
            ruta_completa2_3des = os.path.join(rutaclaves, key_decrypt_3des)
            # Abrimos el fichero con la clave y leemos su contenido
            with open(ruta_completa2_3des, 'r') as file2_3des:
                contenidoclave_3des = file2_3des.read()
            # Finalmente desencriptamos el contenido del fichero seleccionado con la clave y el fichero elegidos
            decrypted_message_3des = f.decrypt_message_3des(contenido2_3des, contenidoclave_3des)

            return render_template('csimetrico.html', 
                                   listado_samba=listado_samba, 
                                   listado_claves=listado_claves, 
                                   listado_archivos_aes=listado_archivos_aes, 
                                   contenido_aes=contenido_aes, 
                                   listado_archivos_3des=listado_archivos_3des, 
                                   contenido_3des=contenido_3des, 
                                   decrypted_message_3des=decrypted_message_3des,
                                   mode_aes=mode_aes, 
                                   mode_3des=mode_3des)

        elif mode_aes == 'subir_samba':
            
            ruta_completa2_aes = os.path.join(rutaclaves, key_decrypt_aes)
            ruta_completa_aes = os.path.join(ruta, archivo2_aes)
            listado_archivos_aes = f.listar(ruta)
            listado_claves = f.listarclaves(rutaclaves)
            listado_archivos_3des = f.listar(ruta)
            listado_samba = f.listar_samba(smb_connection)
            listado_archivos_aes = f.listar(ruta)
            f.cargar_samba(ruta_completa_aes,smb_connection)
            f.cargar_samba(ruta_completa2_aes,smb_connection)
            print("Listado actualizado in the night:", listado_samba)

            return render_template('csimetrico.html', 
                                   listado_samba=listado_samba, 
                                   listado_claves=listado_claves, 
                                   listado_archivos_aes=listado_archivos_aes, 
                                   contenido_aes=contenido_aes, 
                                   listado_archivos_3des=listado_archivos_3des, 
                                   contenido_3des=contenido_3des,  
                                   mode_aes=mode_aes,
                                   mode_samba=mode_samba, 
                                   mode_3des=mode_3des)
        elif 'archivo_samba' in request.form and 'mode_samba' in request.form:
        
            listado_archivos_aes = f.listar(ruta)
            listado_claves = f.listarclaves(rutaclaves)
            listado_archivos_3des = f.listar(ruta)
            listado_samba = f.listar_samba(smb_connection)

            if request.form['mode_samba'] == 'descargar_samba':
                # Obtiene el fichero seleccionado en el desplegable con su ruta completa
                archivo_samba_seleccionado = request.form['archivo_samba']
                clave_samba_seleccionado = request.form['clave_samba']
                local_file_path = f.descargar_sambaclave(smb_connection, clave_samba_seleccionado)
                # Llamamos a la función download_samba para descargar el archivo desde Samba
                local_file_path = f.descargar_samba(smb_connection, archivo_samba_seleccionado)
                listado_archivos_aes = f.listar(ruta)
                listado_claves = f.listarclaves(rutaclaves)
                listado_archivos_3des = f.listar(ruta)
                listado_samba = f.listar_samba(smb_connection)

        return render_template('csimetrico.html', 
                           listado_samba=listado_samba, 
                           listado_claves=listado_claves, 
                           listado_archivos_aes=listado_archivos_aes, 
                           contenido_aes=contenido_aes, 
                           listado_archivos_3des=listado_archivos_3des, 
                           contenido_3des=contenido_3des, 
                           mode_aes=mode_aes, 
                           mode_3des=mode_3des)

    return render_template("csimetrico.html",
                           listado_samba=listado_samba, 
                           listado_claves=listado_claves, 
                           listado_archivos_aes=listado_archivos_aes, 
                           listado_archivos_3des=listado_archivos_3des
                           )
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
