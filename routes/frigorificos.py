# Librerias
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.frigorifico import Frigorifico
from utils.db import session
from flask_login import login_required

# variables globales
# permite que app llame a sus rutas desde blueprint
frigorificos = Blueprint("frigorificos", __name__)



# un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@frigorificos.route("/frigorificos")
@login_required
def vista_frigorificos():
    listaFrigorifico = session.query(Frigorifico).all()  # lista de frigoríficos
    return render_template("/vistas/vistafrigorificos.html", frigorificos=listaFrigorifico)


@frigorificos.route("/frigorificos/<id>")
@login_required
def vista_modal(id): # vista para mostrar la ventana modal para eliminar un elemento
    frigoid = session.query(Frigorifico).get(id)
    return render_template("/vistas/vistafrigorificos.html", frigoid=frigoid)

#
@frigorificos.route("/nuevo_frigorifico", methods=["POST"])  # pagina y metodo
@login_required
def nuevo_frigorifico():
    # variables que capturan los elementos del formulario
    nombre = request.form["nombre"]
    ciudad = request.form["ciudad"]
    direccion = request.form["direccion"]

    q = session.query(Frigorifico).filter(Frigorifico.nombre == nombre).first() # frigorifico filtrado por nombre
    # instanciamos y agregamos los campos
    if q is None:

        nuevoFrigorifico = Frigorifico(nombre, ciudad, direccion)

        # añadir los datos a la base de datos
        session.add(nuevoFrigorifico)
        session.commit()
        flash(message="Frigorífico creado con éxito", category="success")
        return redirect(url_for("frigorificos.vista_frigorificos"))
    else:
        flash("Frigorífico existente, favor ingrese un frigorífico nuevo ",category="errorFrigorifico")
        return redirect(url_for("frigorificos.vista_frigorificos"))


# aparte de la funcion se puede pasar un atributo id para que la url pase esa informacion
@frigorificos.route("/eliminar_frigorifico/<id>")
@login_required
def eliminar_frigorifico(id):
    idFrigorifico = session.query(Frigorifico).get(id) # filtrado por id
    session.delete(idFrigorifico)
    session.commit()
    flash(message="Frigorífico eliminado con éxito", category="delete")
    return redirect(url_for("frigorificos.vista_frigorificos"))


@frigorificos.route("/editar_frigorifico/<id>", methods=["POST", "GET"])
@login_required
def editar_frigorifico(id):
    idFrigorifico = session.query(Frigorifico).get(id)

    if request.method == "POST":
        nombre = request.form['nombre']
        ciudad = request.form["ciudad"]
        direccion = request.form["direccion"]
        if idFrigorifico.nombre == nombre :
            # actualizando los datos capturados del formulario
            idFrigorifico.ciudad = ciudad
            idFrigorifico.direccion = direccion
            session.commit()
            flash(message="Frigorífico editado con éxito", category="update")
            return redirect(url_for("frigorificos.vista_frigorificos"))
        else:
            q = session.query(Frigorifico).filter(Frigorifico.nombre == nombre).first() # filtrado de frigorifico por nombre
            if q is None: # si la consulta no devuelve un frigorifico con le mismo nombre
                # actualizar los datos
                idFrigorifico.nombre = nombre
                idFrigorifico.ciudad = ciudad
                idFrigorifico.direccion = direccion
                session.commit()
                flash(message="Frigorífico actualizado con éxito", category="update")
                return redirect(url_for("frigorificos.vista_frigorificos"))
            else:
                flash("Ya existe éste Frigorífico")
                return render_template("/formularios/form_editar_frigo.html", frigorifico=idFrigorifico)
    else: # retorna el formulario para editar
        return render_template("/formularios/form_editar_frigo.html", frigorifico=idFrigorifico)
