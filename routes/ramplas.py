# Librerias
from datetime import date, datetime
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required
from models.rampla import Rampla
from utils.db import session, engine
from models.transporte import Transporte
from sqlalchemy import text

# variables globales
ramplas = Blueprint("ramplas", __name__)  # nombre de la ruta que sera llamada en la app
fecha_actual = date.today()  # fecha actual


@ramplas.route(
    '/ramplas')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required  # decorador que solo permite el ingreso de las rutas que esten autenticadas
def vista_ramplas():  # ruta para la vista de las ramplas
    lista_transportes = session.query(Transporte).all()
    with engine.connect() as con:
        lista_ramplas = con.execute(text("""select ramplas.id,ramplas.patente_rampla,ramplas.poliza,ramplas.vencimiento_poliza,date_format(ramplas.vencimiento_poliza,'%d%-%m%-%Y') as vencimiento_orden,date_add(ramplas.vencimiento_poliza,interval -7 day) as fecha_advertencia, transportes.nombre as transporte,ramplas.tara_rampla from ramplas
                                            inner join transportes on transportes.id = ramplas.transporteRampla order by ramplas.vencimiento_poliza asc   """))
    return render_template('/vistas/vistaramplas.html', ramplas=lista_ramplas, transportes=lista_transportes,
                           fechaActual=fecha_actual)  # retorno del archivo html mas las variables necesarias como los transportes


@ramplas.route(
    '/ramplas/<id>')  # un decorador puede hacer rutas para llamar paginas html o tambien para dirigir hacia funciones o metodos
@login_required
def vista_modal(id):
    ramplaid = session.query(Rampla).get(id)
    return render_template('/vistas/vistaramplas.html', ramplaid=ramplaid)


@ramplas.route('/nueva_rampla', methods=["POST"])
@login_required
def nueva_rampla():
    # variables que capturan los elementos del formulario
    poliza = request.form["poliza"]
    vencimiento = request.form["vencimiento"]
    patente = request.form["patente"]
    tara = request.form["tara"]
    transporte = request.form.get('idTransporte')
    fecha_format = datetime.strptime(vencimiento, '%Y-%m-%d').date()

    # consulta para saber si hay una patente igual en la base de datos
    q = session.query(Rampla).filter(Rampla.patente_rampla == patente).first()
    if fecha_format < fecha_actual:
        flash("La fecha de vencimiento no puede ser menor al día actual", 'errorFecha')
        return redirect(url_for("ramplas.vista_ramplas"))
    else:
        if q is None:  # condicional: si no existe una rampla con la misma patente
            # creacion del objeto nueva rampla
            nuevaRampla = Rampla(poliza, vencimiento, patente, tara, transporte)
            session.add(nuevaRampla)  # añadir el objeto a la base de datos
            session.commit()  # ejecutar la sentencia
            flash(message="Rampla creada con éxito", category="success")
            return redirect(url_for('ramplas.vista_ramplas'))
        else:
            flash("patente existente, ingrese una patente nueva", 'errorPatente')
            return redirect(url_for("ramplas.vista_ramplas"))


@ramplas.route('/eliminar_rampla/<id>')
@login_required
def eliminar_rampla(id):
    id_rampla = session.query(Rampla).get(id)  # filtrar la rampla por id
    session.delete(id_rampla)  # eliminar la sesion
    session.commit()

    flash(message="Rampla eliminada con éxito", category="delete")
    return redirect(url_for("ramplas.vista_ramplas"))


@ramplas.route('/editar_rampla/<id>', methods=["POST", "GET"])  # pagina y metodo
@login_required
def editar_rampla(id):
    id_rampla = session.query(Rampla).get(id)  # filtrar la rampla por id

    if request.method == "POST":
        lista_transportes = session.query(Transporte).all()
        # variables que almacenan los elementos de los formularios
        patente = request.form["patente"]
        vencimiento = request.form["vencimiento"]
        fecha_format = datetime.strptime(vencimiento, '%Y-%m-%d').date()
        tara = request.form["tara"]
        poliza = request.form["poliza"]
        transporte = request.form.get("idTransporte")

        if fecha_format < fecha_actual:

            flash("La fecha de vencimiento no puede ser menor al día actual", 'errorFecha')
            return render_template('formularios/form_editar_rampla.html', rampla=id_rampla,
                                   transportes=lista_transportes)

        if id_rampla.patente_rampla == patente:  # si la rampla en la rampla filtrada por id es igual al capturado por el formulario
            # actualizando los datos
            id_rampla.poliza = poliza
            id_rampla.vencimiento_poliza = vencimiento
            id_rampla.tara_rampla = tara
            id_rampla.transporteRampla = transporte
            session.commit()
            flash(message="Rampla actualizada con éxito", category="update")
            return redirect(url_for("ramplas.vista_ramplas"))
        else:
            q = session.query(Rampla).filter(Rampla.patente_rampla == patente).first()
            if q is None:
                # actualizando los datos
                id_rampla.patente_rampla = patente
                id_rampla.poliza = poliza
                id_rampla.vencimiento_poliza = vencimiento
                id_rampla.tara_rampla = tara
                id_rampla.transporteRampla = transporte
                session.commit()
                flash(message="Rampla actualizada con éxito", category="update")
                return redirect(url_for("ramplas.vista_ramplas"))
            else:
                flash("Ya existe ésta rampla", 'errorPatente')
                return render_template('formularios/form_editar_rampla.html', rampla=id_rampla,
                                       transportes=lista_transportes)


    else:
        lista_transportes = session.query(Transporte).all()
        return render_template('formularios/form_editar_rampla.html', rampla=id_rampla, transportes=lista_transportes)
