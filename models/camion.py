# Libererias
from utils.db import Base
from sqlalchemy import Column, Integer,String, ForeignKey,Date
from sqlalchemy.orm import relationship


class Camion(Base): # creacion de tablas para la base de datos
    __tablename__ = 'camiones'
    id = Column(Integer,primary_key=True)
    patente_camion = Column(String(8),nullable=False)
    marca = Column(String(50),nullable=False)
    poliza = Column(String(50),nullable=False)
    vencimiento_poliza = Column(Date,nullable=False)
    tara_camion = Column(Integer,nullable=False)
    
    # CLAVES FORANEAS
    transporteCamion = Column(Integer,ForeignKey('transportes.id'))

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    camionConductores = relationship('Conductor')

    # Metodo constructor
    def __init__(self,patente,marca,poliza,vcto,tara,transporte):
        self.patente_camion = patente
        self.marca = marca
        self.poliza = poliza
        self.vencimiento_poliza = vcto
        self.tara_camion = tara
        self.transporteCamion = transporte
        
    def __str__(self):
        return " Camion: {},{}".format(self.marca,self.patente_camion)

    