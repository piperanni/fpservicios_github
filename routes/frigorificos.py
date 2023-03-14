from flask import Blueprint, render_template

frigorificos = Blueprint('frigorificos', __name__)  # permite que app llame a sus rutas desde blueprint


@frigorificos.route('/')  # ahora las rutas ya no son app.route
def home():
    return render_template('index.html')


@frigorificos.route('/actualizar')
def actualizar():
    return render_template('actualizar.html')

@frigorificos.route('/nuevo_frigorifico') # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
def nuevo_frigorifico():
    return "creando nuevo frigorifico"

@frigorificos.route('/eliminar')
def eliminar():
    return "eliminando un frigorifico"

