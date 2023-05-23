from utils.db import Base
from sqlalchemy import Integer, String, Column
from  sqlalchemy.orm import relationship

class Status(Base):
    __tablename__ = "status_embarques"
    id = Column(Integer,primary_key=True)
    nombre = Column(String(50),nullable=False)
    descripcion = Column(String(100),nullable=False)

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    estadoEmbarques = relationship('Embarque')

    def __init__(self,nombre,descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return " Status: {},{}".format(self.nombre,self.descripcion)
        