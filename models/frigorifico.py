from sqlalchemy import Column,Integer,String

from utils.db import Base


class Frigorifico(Base):
    __tablename__ = "frigorifico"
    __table_args__ = {'sqlite_autoincrement':True}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100),nullable=False)
    descripcion = Column(String(100),nullable=False)

    def __int__(self,nombre,descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return " frigorifico: {},{}".format(self.nombre,self.descripcion)
