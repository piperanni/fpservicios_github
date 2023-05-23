from utils.db import Base
from sqlalchemy import Column, Integer,String, ForeignKey,Date
from sqlalchemy.orm import relationship


class Rampla(Base): # creacion de la tabla para la base de datos
    __tablename__ = 'ramplas'
    id = Column(Integer,primary_key=True)
    poliza = Column(String(50),nullable=False)
    vencimiento_poliza = Column(Date,nullable=False)
    patente_rampla = Column(String(8),nullable=False)
    tara_rampla = Column(Integer,nullable=False)
    # CLAVES FORANEAS
    transporteRampla = Column(Integer,ForeignKey('transportes.id',ondelete='CASCADE'))

    # RELACIONES CON LAS TABLAS QUE HEREDAN SU CLAVE PRIMARIA
    ramplaConductores = relationship('Conductor',cascade="all, delete-orphan") # cascade="all, delete"

    # metodo constructor
    def __init__(self,poliza,vcto_poliza,patente_rampla,tara_rampla,id_transporte):
        self.poliza = poliza
        self.vencimiento_poliza = vcto_poliza
        self.patente_rampla = patente_rampla
        self.tara_rampla = tara_rampla
        self.transporteRampla = id_transporte
        
    def __str__(self):
        return " Rampla: {},{}".format(self.id,self.patente_rampla)