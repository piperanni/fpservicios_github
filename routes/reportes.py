# Librerias
from datetime import date
from flask import Blueprint, render_template
import json
import plotly.utils
from flask_login import login_required
from sqlalchemy import text
from utils.db import engine
import pandas as pd
import plotly.express as px


reportes = Blueprint("reportes", __name__)

@reportes.route("/reporte_mensual")
@login_required
def reporte_mensual():
    # lista de meses
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
             'Noviembre', 'Diciembre']

    hoy = date.today() # fecha actual
    mes_actual = meses[hoy.month-1] # mes actual
    mes_anterior = meses[hoy.month-2] # mes anterior

    # consultas sql que devuelven la cantidad de embarques mensuales filtrado por destino

    # consulta sql para el mes actual
    consultaSQL = text(
        "select destinos.nombre as Destino, count(*) as Numero_De_Embarques from embarques inner join destinos on "
        "embarques.destinosId = destinos.id where embarques.fecha_embarque like '{}-%{}%' group by destinos.nombre "
        "".format(hoy.year,hoy.month))

    # consutla sql para el mes anterior
    consultaSQL2 = text(
        "select destinos.nombre as Destino, count(*) as Numero_De_Embarques from embarques inner join destinos on "
        "embarques.destinosId = destinos.id where embarques.fecha_embarque like '{}-%{}%' group by destinos.nombre "
        "".format(hoy.year,hoy.month-1))

    # consultas sql que devuelven la cantidad de embarques mensuales filtrado por transporte
    # consulta para el mes actual
    consultaSQL3 = text(
        "select transportes.nombre as Transporte , count(*) as Total_Por_Mes from transportes inner join conductores "
        "on conductores.transporteConductor = transportes.id inner join embarques on embarques.conductoresId = "
        "conductores.id where embarques.fecha_embarque like '{}-0{}%' group by Transporte".format(hoy.year, hoy.month))

    # consulta para el mes anterior
    consultaSQL4 = text(
        "select transportes.nombre as Transporte , count(*) as Total_Por_Mes from transportes inner join conductores "
        "on conductores.transporteConductor = transportes.id inner join embarques on embarques.conductoresId = "
        "conductores.id where embarques.fecha_embarque like '{}-0{}%' group by Transporte".format(hoy.year, hoy.month-1))

    # creacion dataframe para crear los gráficos
    with engine.begin() as conn:

        # dataframes por destino
        df_mes_anterior = pd.read_sql_query(sql=consultaSQL, con=conn)
        df_mes_actual = pd.read_sql_query(sql=consultaSQL2, con=conn)

        # dataframes por transporte
        df_mes_actual_total_transporte = pd.read_sql_query(sql=consultaSQL3, con=conn)
        df_mes_anterior_total_transporte = pd.read_sql_query(sql=consultaSQL4, con=conn)

    # creacion grafico de tipo barra
    # graficos por destinos
    graf1 = px.bar(df_mes_anterior, x="Destino", y="Numero_De_Embarques",color="Destino")
    graf2 = px.bar(df_mes_actual, x="Destino", y="Numero_De_Embarques",color="Destino")

    # graficos por transporte
    graf3 = px.bar(df_mes_actual_total_transporte, x="Transporte", y="Total_Por_Mes",color="Transporte")
    graf4 = px.bar(df_mes_anterior_total_transporte, x="Transporte", y="Total_Por_Mes",color="Transporte")

    # graficos pasados a formato json para reproducirse en html
    graf1Json = json.dumps(graf1, cls=plotly.utils.PlotlyJSONEncoder)
    graf2Json = json.dumps(graf2, cls=plotly.utils.PlotlyJSONEncoder)
    graf3Json = json.dumps(graf3, cls=plotly.utils.PlotlyJSONEncoder)
    graf4Json = json.dumps(graf4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("graficos/reporte_mensual.html", graph1JSON=graf1Json, graph2JSON=graf2Json,graph3JSON=graf3Json,graph4JSON=graf4Json, meses = [mes_anterior, mes_actual])
