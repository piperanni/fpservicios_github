# Librerias
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.camion import Camion
from utils.db import session, engine
from models.transporte import Transporte
from sqlalchemy import text




# variables globales
# permite que la app llame a sus rutas con blueprint
camiones = Blueprint('camiones', __name__)
fecha_actual = date.today()


@camiones.route('/camiones')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required # decorador para que solo se pueda acceder a la ruta si existe un usuario logeado
def vista_camiones():
    lista_transportes = session.query(Transporte).all()
    # consulta sql personalizada
    with engine.connect() as con:
        lista_camiones = con.execute(text("""select camiones.id,camiones.patente_camion,camiones.marca,camiones.vencimiento_poliza as vencimiento,transportes.nombre as transporte,date_format(camiones.vencimiento_poliza,'%d%-%m%-%Y') as vencimiento_orden,date_add(camiones.vencimiento_poliza,interval -7 day) as fecha_advertencia ,camiones.poliza,camiones.tara_camion from camiones
                        inner join transportes on transportes.id = camiones.transporteCamion order by vencimiento_poliza asc """))

    return render_template('/vistas/vistacamiones.html', camiones=lista_camiones, transportes=lista_transportes,
                           fechaActual=fecha_actual)


@camiones.route('/camiones/<id>')
@login_required
def vista_modal(id): # ruta para enviar los datos a la ventana modal
    camion_by_id = session.query(Camion).get(id)
    return render_template('/vistas/vistacamiones.html', camion=camion_by_id)


@camiones.route('/nuevo_camion', methods=["POST"])  # pagina y metodo
@login_required
def nuevo_camion(): # ruta para agregar un nuevo camion
    # variables del formulario
    marca = request.form["marca"]
    poliza = request.form["poliza"]
    vencimiento = request.form["vencimiento"]
    fecha_format = datetime.strptime(vencimiento, '%Y-%m-%d').date()
    transporte = request.form.get('idTransporte')
    patente = request.form["patente"]
    tara = request.form["tara"]

    # lista del camion filtrado por la patente
    q = session.query(Camion).filter(Camion.patente_camion == patente).first()

    if fecha_format < fecha_actual:  # condicional: si la fecha de vencimiento de la poliza es menor a la fecha actual
        flash("La fecha de vencimiento no puede ser menor al día actual", 'errorFecha')
        return redirect(url_for("camiones.vista_camiones"))

    if q is None:  # condicional: si encuentra un camion con la misma patente escrita en el formulario
        nuevoCamion = Camion(patente, marca, poliza, vencimiento, tara, transporte)
        session.add(nuevoCamion)
        session.commit()
        flash(message="Camión agregado con éxito", category="success")
        return redirect(url_for("camiones.vista_camiones"))
    else:
        flash("patente existente, favor ingrese una patente nueva", 'errorPatente')
        return redirect(url_for("camiones.vista_camiones"))


@camiones.route('/eliminar_camion/<id>')  # pagina y metodo
@login_required
def eliminar_camion(id): # ruta para eliminar un camión
    id_camion = session.query(Camion).get(id)  # busca el camion por el id
    session.delete(id_camion)  # elimina el camión
    session.commit()  # se ejecuta la accion de eliminar

    flash(message="Camión eliminado con éxito", category="delete")  # mensaje flash que permite ejecutar un mensaje
    return redirect(url_for("camiones.vista_camiones"))


@camiones.route('/editar_camion/<id>', methods=["POST", "GET"])  # pagina y metodo
@login_required
def editar_camion(id): # rutas para editar
    id_camion = session.query(Camion).get(id)

    if request.method == "POST":
        lista_transportes = session.query(Transporte).all()
        # capturando varaibles del formulario
        patente = request.form["patente"]
        vencimiento = request.form["vencimiento"]
        fecha_format = datetime.strptime(vencimiento, '%Y-%m-%d').date()
        marca = request.form["marca"]
        poliza = request.form["poliza"]
        tara = request.form["tara"]
        transporte = request.form.get("idTransporte")

        if fecha_format < fecha_actual:  # condicional: si la fecha de vencimiento es mejor a la fecha actual

            flash("La fecha de vencimiento no puede ser menor al día actual", 'errorFecha')
            return render_template('formularios/form_editar_camion.html', camion=id_camion, transportes=lista_transportes)

        if id_camion.patente_camion == patente: # condicional si la patente del camion filtrado por id es igual al capturado por el formulario
            # actualizar los datos
            id_camion.marca = marca
            id_camion.poliza = poliza
            id_camion.vencimiento_poliza = vencimiento
            id_camion.tara_camion = tara
            id_camion.transporteCamion = transporte
            session.commit() # ejecutar la actualizacion

            flash(message="Camión actualizado con éxito", category="update") # mensaje de exito
            return redirect(url_for("camiones.vista_camiones")) # retorna a la vista de camiones
        else:
            q = session.query(Camion).filter(Camion.patente_camion == patente).first() # consulta para obtener una lista de camiones con la misma patente
            if q is None: # condicional: si no hay camiones con la patente capturada en el formulario
                # actualizar datos
                id_camion.patente_camion = patente
                id_camion.marca = marca
                id_camion.poliza = poliza
                id_camion.vencimiento_poliza = vencimiento
                id_camion.tara_camion = tara
                id_camion.transporteCamion = transporte
                session.commit() # ejecuta la accion de actualizar

                flash(message="Camión actualizado con éxito", category="update")
                return redirect(url_for("camiones.vista_camiones"))

            else:
                flash("Ya existe ésta camión", 'errorPatente')
                return render_template('formularios/form_editar_camion.html', camion=id_camion,
                                       transportes=lista_transportes)
    else: # devuelve la ruta para el formulario
        lista_transportes = session.query(Transporte).all()
        return render_template('formularios/form_editar_camion.html', camion=id_camion, transportes=lista_transportes)
