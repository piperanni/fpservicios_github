from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# paremetros conexion
usuario = "root"
contrasena = "Mi911777"
puerto = "3307"
baseDato = "embarques_db"

# cadena de conexion
cadena_conexion= "mysql+pymysql://{}:{}@localhost:{}/{}".format(usuario,contrasena,puerto,baseDato)

#engine = create_engine("mysql+pymysql://root:Mi911777@localhost:3307/contactsdb")
engine = create_engine(cadena_conexion)

# sesion para poder hacer transacciones

Session = sessionmaker(bind=engine)
session = Session()

# vinculacion base se encargar de vincular y crear las tablas y mapear
Base = declarative_base()
