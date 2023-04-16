from flask import Flask, render_template, jsonify,send_file, request,send_from_directory
import os
from datetime import datetime
import requests
import glob
import fnmatch
import urllib.parse

from src.components.savexls import guardar_en_excel

app = Flask(__name__)

@app.route('/')

@app.route("/")
def index():
    path = "src/files"
    archivos = os.listdir(path)
    return render_template("index.html")


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


@app.route('/descargar/<filename>')
def descargar_archivo(filename):
    archivo_path = 'src/files/3105487076/' + filename
    return send_file(archivo_path, as_attachment=False)





from datetime import datetime

import os
import glob
import fnmatch

import os
import glob
import fnmatch
import re
from datetime import datetime
@app.route('/buscar_archivos/<folder>')
def buscar_archivos(folder):
    path = "src/files/"+folder  # replace with the path to your folder
    fecha = request.args.get('mes', '')
    
    trimestres = {
        'enero': 'ene-mar',
        'febrero': 'ene-mar',
        'marzo': 'ene-mar',
        'abril': 'abr-jun',
        'mayo': 'abr-jun',
        'junio': 'abr-jun',
        'julio': 'jul-sep',
        'agosto': 'jul-sep',
        'septiembre': 'jul-sep',
        'octubre': 'oct-dic',
        'noviembre': 'oct-dic',
        'diciembre': 'oct-dic',
    }
    
    mes_regex = r'\d{9}_(' + '|'.join(trimestres.values()) + ')\.xlsx$'
    
    files = []
    for file_path in glob.glob(os.path.join(path, '*')):
        if os.path.isfile(file_path):
            match = re.search(mes_regex, os.path.basename(file_path))
            if match:
                trimestre = match.group(1)
                modified_time = os.path.getmtime(file_path)
                modified_time_str = datetime.fromtimestamp(modified_time).strftime("%d/%m/%Y")
                if trimestres.get(fecha) == trimestre:
                    files.append({
                        'name': os.path.basename(file_path),
                        'modified_time': modified_time_str,
                        'trimestre': trimestre,
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


@app.route('/ver_archivos/<archivo>')
def ver_archivos(archivo):
    archivo = request.args.get('archivo', '')
   # nombre_archivo = os.path.basename(archivo)
    directorio_archivo = os.path.dirname(archivo)
   
    return send_from_directory(directory='src/files/3105487076', path= "3105487076_ene-mar.xlsx")





if __name__ == '__main__':
    app.run()