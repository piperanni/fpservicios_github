from utils.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Destino(Base):
    __tablename__ = 'destinos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    destinoEmbarques = relationship('Embarque')


    def __init__(self,nombre):
        self.nombre = nombre


    def __str__(self):
        return " Destino: {}".format(self.nombre)
