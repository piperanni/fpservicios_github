# Librerias

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from utils.db import session
from models.conductor import Conductor
from models.transporte import Transporte
from models.camion import Camion
from models.rampla import Rampla
from utils.db import engine
from flask_login import login_required

# variables globales
conductores = Blueprint('conductores', __name__)  # permite que app llame a sus rutas desde blueprint


@conductores.route(
    '/conductores')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required
def vista_conductores():  # ruta para ver una lista de conductores

    # listas llamados por el orm SQLalchemy
    lista_transportes = session.query(Transporte).all()
    lista_patente_camion = session.query(Camion).all()
    lista_patente_rampla = session.query(Rampla).all()
    with engine.connect() as con:
        lista_conductores = con.execute(text("""SELECT conductores.id,conductores.nombre,conductores.apellido,conductores.rg,transportes.nombre as transporte,camiones.patente_camion,ramplas.patente_rampla FROM conductores
                                                inner join transportes on transportes.id = conductores.transporteConductor
                                                inner join camiones on camiones.id = conductores.camionConductor
                                                inner join ramplas on ramplas.id = conductores.ramplaConductor"""))

    return render_template('/vistas/vistaconductores.html', conductores=lista_conductores,
                           transportes=lista_transportes, patenteCamiones=lista_patente_camion,
                           patenteRamplas=lista_patente_rampla)


@conductores.route('/conductores/<id>')
@login_required
def vista_modal(id): # ruta para ver una ventana modal para confirmar la eliminacion de un elemento
    conductorid = session.query(Conductor).get(id)
    return render_template('/vistas/vistaconductores.html', conductorid=conductorid)


@conductores.route('/nuevo_conductor', methods=["POST"])  # pagina y metodo
@login_required
def nuevo_conductor():
    # variables que capturan los elementos escritos en un formulario

    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    rg = int(request.form["rg"])
    transporte = request.form.get('idTransporte')
    patenteCamion = request.form.get('idPatenteCamion')
    patenteRampla = request.form.get('idPatenteRampla')

    # consulta que devuelve un conductor filtrado por rg( regitro general de identificación en brasil)
    q = session.query(Conductor).filter(Conductor.rg == rg).first()

    if q is None: # condicional: si la consulta no devuelve un conductor con el mismo regitro de identidad

        # creacion de un objeto conductor para insertarlo a la base de datos
        nuevoConductor = Conductor(nombre, apellido, rg, transporte, patenteCamion, patenteRampla)
        session.add(nuevoConductor)
        session.commit()
        flash(message="Conductor creado con éxito", category="success")
        return redirect(url_for("conductores.vista_conductores"))
    else:
        flash("Registro existente, favor ingrese RG correcto", category="errorRg")
        return redirect(url_for("conductores.vista_conductores"))


@conductores.route('/eliminar_conductor/<id>')
@login_required
def eliminar_conductor(id):
    id_conductor = session.query(Conductor).get(id)  # busca el conductor por el id para poder eliminarlo
    session.delete(id_conductor)  # elimina el camión
    session.commit()  # se ejecuta la accion de eliminar
    flash(message="Conductor eliminado con éxito", category="delete")
    return redirect(url_for("conductores.vista_conductores"))


@conductores.route('/editar_conductor/<id>', methods=["POST", "GET"])
@login_required
def editar_conductor(id):
    idConductor = session.query(Conductor).get(id)

    if request.method == "POST":
        # listas llamados por el orm SQLalchemy
        lista_transportes = session.query(Transporte).all()
        lista_patente_camion = session.query(Camion).all()
        lista_patente_rampla = session.query(Rampla).all()

        # capturar los elementos del formulario en variables
        rg = int(request.form["rg"])
        transporte = request.form.get('idTransporte')
        patenteCamion = request.form.get('idPatenteCamion')
        patenteRampla = request.form.get('idPatenteRampla')
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]

        if idConductor.rg == rg: # condicional: si el rg del conductor filtrado por id es igual al escrito en el formulario:
            # accion de actualizar los elementos del conductor
            idConductor.nombre = nombre
            idConductor.apellido = apellido
            idConductor.transporteConductor = transporte
            idConductor.camionConductor = patenteCamion
            idConductor.ramplaConductor = patenteRampla
            session.commit()
            flash(message="Conductor actualizado con éxito", category="update")
            return redirect(url_for("conductores.vista_conductores"))
        else:
            q = session.query(Conductor).filter(Conductor.rg == request.form["rg"]).first()
            if q is None: # condicional: si no existe un conductor con el mismo registro de identidad entonces:
                # actualizacion de los datos
                idConductor.rg = rg
                idConductor.nombre = nombre
                idConductor.apellido = apellido
                idConductor.transporteConductor = transporte
                idConductor.camionConductor = patenteCamion
                idConductor.ramplaConductor = patenteRampla
                session.commit()
                flash(message="Conductor actualizado con éxito", category="update")
                return redirect(url_for("conductores.vista_conductores"))
            else:
                flash("Ya existe éste Registro general (RG)")
                return render_template("/formularios/form_editar_condu.html", conductor=idConductor,
                                       transportes=lista_transportes, patenteRamplas=lista_patente_rampla,
                                       patenteCamiones=lista_patente_camion)

    else:
        # listas llamados por el orm SQLalchemy
        lista_transportes = session.query(Transporte).all()
        lista_patente_camion = session.query(Camion).all()
        lista_patente_rampla = session.query(Rampla).all()
        return render_template("/formularios/form_editar_condu.html", conductor=idConductor,
                               transportes=lista_transportes, patenteRamplas=lista_patente_rampla,
                               patenteCamiones=lista_patente_camion)
