# Librerias
from sqlalchemy import Column,Integer, ForeignKey,Date
from utils.db import Base

class Embarque(Base): # creacion de tablas para la base de datos
    __tablename__ = 'embarques'
    id = Column(Integer,primary_key=True)
    fecha_embarque = Column(Date,nullable=False)

    # Claves Foraneas
    conductoresId = Column(Integer,ForeignKey('conductores.id'))
    frigorificosId = Column(Integer,ForeignKey('frigorificos.id')) 
    destinosId = Column(Integer,ForeignKey('destinos.id')) 
    fronterasId = Column(Integer,ForeignKey('fronteras.id'))
    statusEmbarquesId = Column(Integer,ForeignKey('status_embarques.id'))

    # metodo constructor
    def __init__(self,fecha,conductor,frigorifico,destino,frontera,status):
        self.fecha_embarque = fecha
        self.conductoresId = conductor
        self.frigorificosId = frigorifico
        self.destinosId = destino
        self.fronterasId = frontera
        self.statusEmbarquesId = status

    def __str__(self):
        return " embarque: {}".format(self.id)