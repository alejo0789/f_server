from flask import Flask, render_template, jsonify,send_file, request
import os
from datetime import datetime
import requests
import glob
import fnmatch
import re
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import users
import json

from src.components.savexls import guardar_en_excel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://userdb_r5u6_user:hAYrARqcSxV8zkxzMt2QhT1Tl5vpP1Ea@dpg-cg9k6epmbg54mbfpjv0g-a.oregon-postgres.render.com/userdb_r5u6"
#"postgresql://userdb_r5u6_user:hAYrARqcSxV8zkxzMt2QhT1Tl5vpP1Ea@dpg-cg9k6epmbg54mbfpjv0g-a/userdb_r5u6"
#"postgresql://userdb_r5u6_user:hAYrARqcSxV8zkxzMt2QhT1Tl5vpP1Ea@dpg-cg9k6epmbg54mbfpjv0g-a.oregon-postgres.render.com/userdb_r5u6" #ojo modificar 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/')

@app.route("/")
def index():
    path = "src/files"
    archivos = os.listdir(path)
    return render_template("index.html")



@app.route("/registro")
def registro():

    return render_template("registro.html")



@app.route("/add_user", methods=['POST'])


def add_user():
    name = request.form['nombre']
    tel = request.form['telefono']
    email = request.form['email']
    password = request.form['password']
    #email = request.form['email']
    user = users(name=name, email=email, telephone=tel, password=password)
    db.session.add(user)
    db.session.commit()

    #send data to whatsapp and get notification welcome
    url_api_Wp="https://wp-api-render.onrender.com/whatsapp"
    #url_api_Wp = "http://localhost:3000/whatsapp"
    data = {"texto": "hola", "number": tel}

    json_data = json.dumps(data)
    print(json_data)
    headers = {'Content-type': 'application/json'}

    response = requests.post(url_api_Wp, data=json_data, headers=headers)

    print(response)
    return 'User registered successfully'


@app.route('/getfiles/<numero>')
def get_files(numero):
    folder_path = os.path.join('src', 'files', numero)
    files = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                file_path = os.path.join(folder_path, filename)
                modified_time = os.path.getmtime(file_path)
                modified_time_str = datetime.fromtimestamp(modified_time).strftime("%d/%m/%Y")
                files.append({
                    'name': filename,
                    'modified_time': modified_time_str,
                    'file_path': file_path,
                })
        files = sorted(files, key=lambda f: f['modified_time'], reverse=True)
    return render_template('archivos.html', archivos=files)
    
   # return jsonify(files)


@app.context_processor
def utility_processor():
    def format_datetime(value, format="%d/%m/%Y"):
        return datetime.fromtimestamp(value).strftime(format)
    return dict(format_datetime=format_datetime)


@app.route('/listfiles')
def listar_archivos():
    api_url = 'https://f-server2.onrender.com/getfiles'
    response = requests.get(api_url)
    archivos = response.json()
    return render_template('archivos.html', archivos=archivos)


@app.route('/descargar/<archivo_name>')
def descargar_archivo(archivo_name):
    match = re.search(r'^(\d+)_', archivo_name)
    if match:
     folder = match.group(1)
    else:
      folder=573105487076
    #folder_path = os.path.join('src', 'files', folder, archivo)
    # Verificar que la ruta del archivo existe
    # y extraer el nombre del archivo de la ruta
   


    # Usar la función send_file para enviar el archivo al usuario
    return send_file("src/files/"+folder+"/"+archivo_name, as_attachment=True)


@app.route('/descargar2/<ruta_archivo>')
def descargar_archivo2(ruta_archivo):
    folder_path = os.path.join(ruta_archivo)
    # Verificar que la ruta del archivo existe
    # y extraer el nombre del archivo de la ruta
    nombre_archivo = os.path.basename(ruta_archivo)
    print(ruta_archivo)
    print("Nombre "+nombre_archivo)
    ruta_archivostring=ruta_archivo
    return send_file('src/files/573105487076/573105487076_ene-mar.xlsx', as_attachment=True)

@app.route('/ver_archivo/<path:archivo>')
def ver_archivo(archivo):

    return render_template('ver_archivo.html', archivo=archivo)

@app.route('/mostrar_archivo/<archivo>')
def mostrar_archivo(archivo):
    print("entrando")
    return send_file('src/files/573105487076/'+archivo, as_attachment=True)


from datetime import datetime

import os
import glob
import fnmatch

@app.route('/buscar_archivos')
def buscar_archivos():
    path = "src/files"  # replace with the path to your folder
    nombre_archivo = request.args.get('nombre', '')
    files = []
    for file_path in glob.glob(os.path.join(path, '*')):
        if os.path.isfile(file_path) and fnmatch.fnmatch(os.path.basename(file_path), f'*{nombre_archivo}*'):
            modified_time = os.path.getmtime(file_path)
            modified_time_str = datetime.fromtimestamp(modified_time).strftime("%d/%m/%Y")
            files.append({
                'name': os.path.basename(file_path),
                'modified_time': modified_time_str,
                'file_path': file_path,
            })
    return render_template('archivos.html', archivos=files)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    texto = data['text']
    number= data['numero']
    guardar_en_excel(texto, number)
   
    # Procesar la información recibida como sea necesario
    # ...

    # Devolver una respuesta JSON
    response = {'message': 'Usuario registrado exitosamente '+ texto}
    return jsonify(response)


@app.route('/terminos_y_condiciones')
def terminos():
   
    return render_template('terminos.html')



if __name__ == '__main__':
    app.run()
