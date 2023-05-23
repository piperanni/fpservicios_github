# Librerias
from flask import Flask, redirect, url_for, request, render_template, flash
from routes.frigorificos import frigorificos
from config import config
from routes.embarques import embarques
from routes.transportes import transportes
from routes.conductores import conductores
from routes.camiones import camiones
from routes.ramplas import ramplas
from routes.reportes import reportes
from routes.reporteAnual import reportesAnuales
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user
from models.entities.User import User

from models.ModelUser import ModelUser
app = Flask(__name__)
# registros para llamar a las otras rutas fuera de app.py
app.register_blueprint(embarques)
app.register_blueprint(transportes)
app.register_blueprint(conductores)
app.register_blueprint(camiones)
app.register_blueprint(ramplas)
app.register_blueprint(reportes)
app.register_blueprint(reportesAnuales)
app.register_blueprint(frigorificos) # permite llamar a las rutas almacenadas en utils


db = MySQL(app)
login_manager_app = LoginManager(app)
app.config.from_object(config['development'])
#csrf.init_app(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)


@app.route('/')
def index():
    return redirect(url_for('vista_login'))
@app.route('/login', methods=['GET', 'POST'])
def vista_login():
    if request.method == 'POST':
        user = User(id=0, username=request.form['username'], password=request.form['password'])
        logged_user = ModelUser.login(db, user)
        # comprobacion de usuarios
        if logged_user != None:
            # comprobacion de password
            if logged_user.password == True:
                login_user(logged_user)
                return redirect(url_for('embarques.vista_embarques'))
            else:
                flash("usuario o contraseña invalidos")
                return render_template('/auth/login.html')

        else:
            flash("usuario o contraseña invalidos")
            return render_template('/auth/login.html')
    else:
        return render_template('/auth/login.html')

@app.route('/logout')
def logout(): # metodo para salir de una sesion
    logout_user()
    return  redirect(url_for('vista_login'))


