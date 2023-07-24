from flask import Flask, render_template, jsonify,send_file, request,send_from_directory
import os
from datetime import datetime
import requests
import glob
import fnmatch
import re
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Users, Transaction
import json
import datetime as dt

from src.components.savexls import guardar_en_excel, separar_texto_y_numeros, define_tipo
from flask_login import LoginManager



#login extenssions

from werkzeug.urls import url_parse
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (render_template, redirect, url_for,
                   request, current_app)





#####################################################

app = Flask(__name__)

app.config['SECRET_KEY'] = '94b3949f15d6bab2d2892bb8decd1e1f7e2b2fb'
login_manager = LoginManager(app)

"in comments due to the online database it is not working"
##########################################################################################
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://userdb_r5u6_user:hAYrARqcSxV8zkxzMt2QhT1Tl5vpP1Ea@dpg-cg9k6epmbg54mbfpjv0g-a.oregon-postgres.render.com/userdb_r5u6"
#"postgresql://userdb_r5u6_user:hAYrARqcSxV8zkxzMt2QhT1Tl5vpP1Ea@dpg-cg9k6epmbg54mbfpjv0g-a/userdb_r5u6"
#"postgresql://userdb_r5u6_user:hAYrARqcSxV8zkxzMt2QhT1Tl5vpP1Ea@dpg-cg9k6epmbg54mbfpjv0g-a.oregon-postgres.render.com/userdb_r5u6" #ojo modificar 
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#db = SQLAlchemy(app)

#with app.app_context():
 #   db.create_all()
#########################################################################################



"""create local connection with posgresql

print('postgresql://'+user+':'+password+'@'+hostname+':'+port+'/'+database)"""

#local connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+user+':'+password+'@'+hostname+':'+port+'/'+database
#fly connection does not working
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:JHfv03AiFBRmDPe@db-money-tracker.fly.dev:5432/money_tracker'

#neon.tech connection 
database="money_tracker"
user='postgres'
hostname="localhost"
password='root'
port="5432"
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://alejo0789:94lGBRCAwHvh@ep-square-dream-61055761.us-east-2.aws.neon.tech/money_tracker'
from sqlalchemy import create_engine

#CONNSTR = f'postgresql://alejo0789:94lGBRCAwHvh@ep-square-dream-61055761.us-east-2.aws.neon.tech/money_tracker'

#engine = create_engine(CONNSTR)
db.init_app(app) 

with app.app_context():
    db.create_all()

########################################################################################
# Mock User class for demonstration purposes to login session

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


# User loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/")
def index():
    return render_template("index.html")
"""
@app.route('/')
@login_required
def home():
    user_id = load_user(request.args.get('user_id')).id
    return 'Logged in as: ' + str(user_id)
"""
@app.route('/terminos_y_condiciones')
def terminos():
   
    return render_template('terminos.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        
        # Perform authentication here, e.g., check against a database
        # You can modify this part to fit your authentication logic

        # For simplicity, we'll use a hard-coded user_id
        if user_id == '12345':
            user = User(user_id)
            login_user(user)
            return redirect('/?user_id=' + user_id)
        else:
            return 'Invalid user ID'
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/registro")
def registro():

    return render_template("registro.html")



@app.route("/add_user", methods=['POST'])


def add_user():

    #cursor = localConnection.conn.cursor()
    
 


    name = request.form['nombre']
    tel = request.form['telefono']
    email = request.form['email']
    password =generate_password_hash(request.form['password'])
    

 
    user = Users(username=name, email=email, phone=tel, password=password)
    db.session.add(user)
    db.session.commit()
  
    #send data to whatsapp and get notification welcome
    url_api_Wp="https://wp-api-render.onrender.com/whatsapp"
    #url_api_Wp = "http://localhost:3000/whatsapp"
    data = {"texto": "hola", "number": tel}

    json_data = json.dumps(data)
    print(json_data)
    headers = {'Content-type': 'application/json'}
   # send whatsapp
    response = requests.post(url_api_Wp, data=json_data, headers=headers)

    print(response)
    return resumen()

#this functions returns the files according with the number 
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

"""
@app.route('/listfiles')
def listar_archivos():
    api_url = 'https://f-server2.onrender.com/getfiles'
    response = requests.get(api_url)
    archivos = response.json()
    return render_template('archivos.html', archivos=archivos)
"""

@app.route('/descargar/<archivo_name>')
def descargar_archivo(archivo_name):
    match = re.search(r'^(\d+)_', archivo_name)
    if match:
     folder = match.group(1)

    # Usar la función send_file para enviar el archivo al usuario
    return send_file("src/files/"+folder+"/"+archivo_name, as_attachment=True)

@app.route('/sendfile/<number>')
def sendfile(number):
    
    folder = number

    fecha_actual = dt.datetime.now()

    # Convertir la fecha actual en una cadena de texto con formato dd/mm/yyyy
    fecha_formateada = fecha_actual.strftime('%d/%m/%Y')
    
    mes_actual = fecha_actual.strftime('%m')
    anio_actual = fecha_actual.strftime('%Y')

    # Crea el nombre del archivo con el número de persona, mes y año actual
    file_name = f"{number}_{mes_actual}_{anio_actual}.xlsx"

    # Usar la función send_file para enviar el archivo al usuario
    return send_file("src/files/"+folder+"/"+file_name, as_attachment=True)
"""
@app.route('/ver_archivo/<path:archivo>')
def ver_archivo(archivo):

    return render_template('ver_archivo.html', archivo=archivo)

@app.route('/mostrar_archivo/<archivo>')
def mostrar_archivo(archivo):
 
    return send_file('src/files/573105487076/'+archivo, as_attachment=True)


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
"""
@app.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    texto = data['text']
    number= data['numero']
    #check if the phone exist in the databse
    user = Users.query.filter_by(phone=number).first()
    if not user:
        response = {'message': 'Debes resgistrarte es muy sencillo, ingresa a www.noteair.com '},404
        return jsonify(response)
       
    #guardar_en_excel(texto, number)

    #call the function from savexls.py to separate text form numbers
    justText, justValue  = separar_texto_y_numeros(texto)
    # Define the type or category of this value (ingreso, ahorro o gasto)
    tipo, texto = define_tipo(texto.lower())
     # Perform the database insertion
    current_timestamp = datetime.utcnow()
    try:
        ingreso_transaction = Transaction(user_id=user.id, category=tipo, amount=justValue,date_time=current_timestamp, description=justText)
        db.session.add(ingreso_transaction)
        db.session.commit()
           # Devolver una respuesta JSON
        response = {'message': 'exitosamente '+ texto}
        return jsonify(response),200
       
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
   




@app.route('/resumen')
#f@login_required
def resumen():
   
    return render_template('resumen.html')

@app.route('/graphs')
def graphs():
   
    return render_template('graphs.html')
if __name__ == '__main__':
    app.run()
