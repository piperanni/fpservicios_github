# Librerias
from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.embarque import Embarque
from utils.db import session,engine
from models.conductor import Conductor
from models.frigorifico import Frigorifico
from models.destino import Destino
from models.frontera import Frontera
from sqlalchemy import text

# varaibles globales
embarques = Blueprint('embarques', __name__)  # permite que app llame a sus rutas desde blueprint
hoy = date.today()

@embarques.route(
    '/embarques')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required
def vista_embarques():

    lista_conductores = session.query(Conductor).all()
    lista_frigorificos = session.query(Frigorifico).all()
    lista_destino = session.query(Destino).all()
    lista_frontera = session.query(Frontera).all()
    with engine.connect() as con:
        lista_estado = con.execute(text("""select * from status_embarques """)).fetchall()
        lista_embarques = con.execute(text("""
        select embarques.id, status_embarques.nombre as status,
        conductores.nombre,conductores.apellido,date_format(fecha_embarque,'%d%-%m%-%Y') as fechaEmbarque,
        transportes.nombre as transporte,ramplas.patente_rampla,camiones.patente_camion,
        frigorificos.nombre as frigorifico,destinos.nombre as destino,fronteras.nombre as frontera
        from conductores 
        inner join camiones  on conductores.camionConductor = camiones.id 
        inner join transportes  on conductores.transporteConductor = transportes.id
        inner join embarques on embarques.conductoresId = conductores.id
        inner join ramplas on conductores.ramplaConductor = ramplas.id
        inner join frigorificos on frigorificos.id = embarques.frigorificosId
        inner join destinos on destinos.id = embarques.destinosId
        inner join fronteras on fronteras.id = embarques.fronterasId
        inner join status_embarques on status_embarques.id = embarques.statusEmbarquesId
        order by fecha_embarque DESC """)).fetchall()

    return render_template('/vistas/vistaembarques.html', embarques=lista_embarques, conductores=lista_conductores,
                               frigorificos=lista_frigorificos, destinos=lista_destino, fronteras=lista_frontera,
                               estados=lista_estado)


@embarques.route(
    '/embarques/<id>')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required
def vista_modal(id):
    with engine.connect() as con:
        embid = con.execute(text("""SELECT embarques.id, conductores.nombre as conductor FROM embarques
        inner join conductores on embarques.conductoresid = conductores.id
        where embarques.id = {}""".format(id))).fetchone()
    return render_template('/vistas/vistaembarques.html', embid=embid)


@embarques.route('/nuevo_embarque', methods=["POST"])
@login_required
def nuevo_embarque():
    # varaibles que capturan los elementos del formulario
    fechaEmbarque = request.form["fecha"]
    fecha_format = datetime.strptime(fechaEmbarque, '%Y-%m-%d').date()

    if fecha_format < hoy:
        flash("No se puede agendar un embarque con fecha anterior al dia actual", category="errorFecha")
        return redirect(url_for('embarques.vista_embarques'))
    else:
        # varaibles que capturan los elementos del formulario
        fechaEmbarque = request.form["fecha"]
        conductor = int(request.form.get('idConductor'))
        frigorifico = int(request.form.get('idFrigo'))
        destino = int(request.form.get('idDestino'))
        frontera = int(request.form.get('idfrontera'))
        ubicacion = int(request.form.get('idUbicacion'))

       # with engine.connect() as con:
           # nuevoEmbarque = con.execute(text("""
              #  INSERT INTO `embarques_db`.`embarques` (`fecha_embarque`, `conductoresId`, `frigorificosId`, `destinosId`, `fronterasId`, `statusEmbarquesId`)
              #  VALUES ('{}', '{}', '{}', '{}', '{}', '{}') """.format(fecha, conductor, frigorifico, destino, frontera,
                                                              # ubicacion)))
           # con.commit()

        nuevoEmbarque = Embarque(fechaEmbarque,conductor,frigorifico,destino,frontera,ubicacion)
        session.add(nuevoEmbarque)
        session.commit()
        flash(message="Embarque creado con éxito", category="success")
        return redirect(url_for('embarques.vista_embarques'))


@embarques.route('/eliminar/<id>')
@login_required
def eliminar_embarque(id):
    idEmbarque = session.query(Embarque).get(id)
    session.delete(idEmbarque)
    session.commit()
    flash(message="Embarque eliminado con éxito", category="delete")
    return redirect(url_for('embarques.vista_embarques'))


@embarques.route('/editar_embarque/<id>', methods=['POST', 'GET'])
@login_required
def editar_embarque(id):
    idEmbarque = session.query(Embarque).get(id)

    if request.method == 'POST':
        # listas
        lista_conductores = session.query(Conductor).all()
        lista_frigorificos = session.query(Frigorifico).all()
        lista_destino = session.query(Destino).all()
        lista_frontera = session.query(Frontera).all()
        with engine.connect() as con:
            lista_estado = con.execute(text("""select * from status_embarques """)).fetchall()
        # variables que capturan los elementos del formulario
        fecha_embarque = request.form["fecha"]
        idConductor = request.form.get("idConductor")
        idFrigo = request.form.get("idFrigo")
        idDestino = request.form.get("idDestino")
        idFrontera = request.form.get("idfrontera")
        idUbicacion = request.form.get("idUbicacion")
        # fecha formateada para poder comparse
        fecha_format = datetime.strptime(fecha_embarque, '%Y-%m-%d').date()

        if fecha_format < hoy:
            flash("No se puede re agendar un embarque con fecha anterior al dia actual")
            return render_template("/formularios/form_editar_embarque.html", embarque=idEmbarque,
                                   conductores=lista_conductores, frigorificos=lista_frigorificos,
                                   destinos=lista_destino, fronteras=lista_frontera, estados=lista_estado)
        else:
            idEmbarque.fecha_embarque = fecha_embarque
            idEmbarque.conductoresId = idConductor
            idEmbarque.frigorificosId = idFrigo
            idEmbarque.destinosId = idDestino
            idEmbarque.fronterasId = idFrontera
            idEmbarque.statusEmbarquesId = idUbicacion
            session.commit()
            flash(message="Embarque actualizado con éxito", category="update")
            return redirect(url_for('embarques.vista_embarques'))

    else:
        lista_conductores = session.query(Conductor).all()
        lista_frigorificos = session.query(Frigorifico).all()
        lista_destino = session.query(Destino).all()
        lista_frontera = session.query(Frontera).all()
        with engine.connect() as con:
            lista_estado = con.execute(text("""select * from status_embarques """)).fetchall()
        return render_template("/formularios/form_editar_embarque.html", embarque=idEmbarque,
                               conductores=lista_conductores, frigorificos=lista_frigorificos,
                               destinos=lista_destino, fronteras=lista_frontera, estados=lista_estado)