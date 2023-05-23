from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from utils.db import Base,session

class Frontera(Base):
    __tablename__ = 'fronteras'
    id = Column(Integer,primary_key=True)
    nombre = Column(String(50),nullable=False)

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    fronteraEmbarques = relationship('Embarque')


    def __init__(self,nombre):
        self.nombre = nombre

    def __str__(self):
        return " Frontera: {}".format(self.nombre)


        
