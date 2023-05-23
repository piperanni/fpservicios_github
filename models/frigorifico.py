from sqlalchemy import Column,Integer,String
from utils.db import Base
from sqlalchemy.orm import relationship

class Frigorifico(Base):
    __tablename__ = "frigorificos"
    
    id = Column(Integer,primary_key=True)
    nombre = Column(String(100),nullable=False)
    ciudad = Column(String(100),nullable=False)
    direccion = Column(String(100),nullable=False)

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    frigorificoEmbarques = relationship('Embarque')


    def __init__(self,nombre,ciudad,direccion):
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion

    def __str__(self):
        return " frigorifico: {},{},{}".format(self.nombre,self.ciudad,self.direccion)
