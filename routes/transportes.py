from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models.transporte import Transporte
from utils.db import session

transportes = Blueprint('transportes', __name__)  # permite que app llame a sus rutas desde blueprint


@transportes.route(
    '/transportes')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required
def vista_transportes():  # ruta para ver la lista de transporte
    lista_transporte = session.query(Transporte).all()
    return render_template('/vistas/vistatransportes.html', transportes=lista_transporte)


@transportes.route(
    '/transportes/<id>')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required
def vista_modal(id):
    transporteid = session.query(Transporte).get(id)  # transporte filtrado por id
    return render_template('/vistas/vistatransportes.html', transp=transporteid)


# Ruta formulario
@transportes.route('/nuevo_transporte', methods=["POST"])  # pagina y metodo formulario
@login_required
def nuevo_transporte():  # ruta para agregar nuevo transporte
    # variables que capturan los elementos del formulario
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    q = session.query(Transporte).filter(
        Transporte.nombre == nombre).first()  # consulta para filtrar transporte por nombre
    # instanciamos y agregamos los campos
    if q is None:  # condicional: si no hay un transporte con el mismo nombre

        nuevoTransporte = Transporte(nombre, direccion)  # instancia de la clase transporte
        session.add(nuevoTransporte)  # agregar un nuevo transporte
        session.commit()
        flash(message="Transporte agregado con éxito", category="success")
        return redirect(url_for("transportes.vista_transportes"))
    else:
        flash("transporte existente, favor ingrese un transporte nuevo ", category="errorTransporte")
        return redirect(url_for("transportes.vista_transportes"))  # "<h1>nombre ya existe</h1"


@transportes.route('/eliminar_transporte/<id>')  # pagina y metodo
@login_required
def eliminar_transporte(id):  # ruta para eliminar un transporte
    idTransporte = session.query(Transporte).get(id)  # filtrar transporte por id
    session.delete(idTransporte)
    session.commit()
    flash(message="Transporte eliminado con éxito", category="delete")
    return redirect(url_for("transportes.vista_transportes"))


@transportes.route('/editar_transporte/<id>', methods=["POST", "GET"])  # pagina y metodo
@login_required
def editar_transporte(id):
    idTransporte = session.query(Transporte).get(id)  # filtrar transporte por id
    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]

        if idTransporte.nombre == request.form["nombre"]:
            idTransporte.direccion = direccion
            session.commit()
            flash(message="Transporte actualizado con éxito", category="update")
            return redirect(url_for("transportes.vista_transportes"))
        else:
            q = session.query(Transporte).filter(Transporte.nombre == nombre).first()  # transporte filtrado por nombre
            if q is None:  # si no existe un nombre en la base de datos igual al capturado en el formulario
                idTransporte.nombre = nombre
                idTransporte.direccion = direccion
                session.commit()
                flash(message="Transporte actualizado con éxito", category="update")
                return redirect(url_for("transportes.vista_transportes"))
            else:
                flash("Ya existe éste transporte")
                return render_template("/formularios/form_editar_transp.html", transporte=idTransporte)


    else:  # devuelve la ruta para mostrar el formulario
        return render_template("/formularios/form_editar_transp.html", transporte=idTransporte)