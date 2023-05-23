from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from utils.db import Base

class Transporte(Base):
    __tablename__ = 'transportes'
    id = Column(Integer,primary_key=True)
    nombre = Column(String(100),nullable=False)
    direccion = Column(String(100),nullable=False)

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    transporteConductores = relationship('Conductor')
    transporteCamiones = relationship('Camion')
    transporteRamplas = relationship("Rampla") # backref=backref('children', passive_deletes=True)

    # metodo constructor
    def __init__(self,nombre,direccion):
        self.nombre = nombre
        self.direccion = direccion

    def __str__(self):
        return " transporte: {},{}".format(self.nombre,self.direccion)
