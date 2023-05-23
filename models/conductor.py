# Librerias
from utils.db import Base
from sqlalchemy import Column, Integer,String, ForeignKey
from sqlalchemy.orm import relationship


class Conductor(Base): # creacion de tabla para la base de datos
    __tablename__ = 'conductores'
    id = Column(Integer,primary_key=True)
    nombre = Column(String(50),nullable=False)
    apellido = Column(String(80),nullable=False)
    rg = Column(Integer,nullable=False)
    
    #   CLAVES FORANEAS
    transporteConductor = Column(Integer,ForeignKey('transportes.id'))
    camionConductor = Column(Integer,ForeignKey('camiones.id'))
    ramplaConductor = Column(Integer,ForeignKey('ramplas.id'))

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    conductorEmbarques = relationship('Embarque')
    # Metodo constructor
    def __init__(self,nombre,apellido,rg,transporte,camion, rampla):
        self.nombre = nombre
        self.apellido = apellido
        self.rg = rg
        self.transporteConductor = transporte
        self.camionConductor = camion
        self.ramplaConductor = rampla
        
    def __str__(self):
        return " conductor: {},{},{}".format(self.nombre,self.camionConductor,self.ramplaConductor)
         
        
    
        
        
