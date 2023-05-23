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

reportesAnuales = Blueprint("reportesAnuales", __name__) # ruta


@reportesAnuales.route("/reporte_anual")
@login_required
def reporte_anual():

    anio_actual = date.today().year # variable de año actual
    anio_anterior = anio_actual-1 # variable de año anterior

    # consultas sql que devuelven la cantidad de embarques anuales filtrado por destino
    consultaSQL = text(
        "select destinos.nombre as Destino, count(*) as Numero_De_Embarques from embarques inner join destinos on "
        "embarques.destinosId = destinos.id where embarques.fecha_embarque like '{}%' group by destinos.nombre "
        "".format(anio_actual)
    )
    consultaSQL2 = text(
        "select destinos.nombre as Destino, count(*) as Numero_De_Embarques from embarques inner join destinos on "
        "embarques.destinosId = destinos.id where embarques.fecha_embarque like '{}%' group by destinos.nombre "
        "".format(anio_anterior)
    )
    # consultas sql que devuelven la cantidad de embarques anuales filtrado por Transporte
    consultaSQL3 = text(
        "select transportes.nombre as Transporte , count(*) as Total_Por_Mes from transportes inner join conductores "
        "on conductores.transporteConductor = transportes.id inner join embarques on embarques.conductoresId = "
        "conductores.id where embarques.fecha_embarque like '{}%' group by Transporte".format(anio_actual)
    )
    consultaSQL4 = text(
        "select transportes.nombre as Transporte , count(*) as Total_Por_Mes from transportes inner join conductores "
        "on conductores.transporteConductor = transportes.id inner join embarques on embarques.conductoresId = "
        "conductores.id where embarques.fecha_embarque like '{}%' group by Transporte".format(anio_anterior)
    )

    # creacion dataframe
    with engine.begin() as conn:
        df_anio_anterior = pd.read_sql_query(sql=consultaSQL, con=conn)
        df_anio_actual = pd.read_sql_query(sql=consultaSQL2, con=conn)
        df_anio_actual_total_transporte = pd.read_sql_query(sql=consultaSQL3, con=conn)
        df_anio_anterior_total_transporte = pd.read_sql_query(sql=consultaSQL4, con=conn)

    # creacion grafico de tipo linea
    graf1 = px.bar(df_anio_anterior, x="Destino", y="Numero_De_Embarques",color="Destino")
    graf2 = px.bar(df_anio_actual, x="Destino", y="Numero_De_Embarques",color="Destino")
    graf3 = px.bar(df_anio_actual_total_transporte, x="Transporte", y="Total_Por_Mes",color="Transporte")
    graf4 = px.bar(df_anio_anterior_total_transporte, x="Transporte", y="Total_Por_Mes",color="Transporte")

    # graficos pasados a formato json para reproducirse en html
    graf1Json = json.dumps(graf1, cls=plotly.utils.PlotlyJSONEncoder)
    graf2Json = json.dumps(graf2, cls=plotly.utils.PlotlyJSONEncoder)
    graf3Json = json.dumps(graf3, cls=plotly.utils.PlotlyJSONEncoder)
    graf4Json = json.dumps(graf4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("graficos/reporte_anual.html", graph1JSON=graf1Json, graph2JSON=graf2Json,
                           graph3JSON=graf3Json, graph4JSON=graf4Json, anios=[anio_anterior, anio_actual])
