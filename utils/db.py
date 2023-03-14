from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#engine = create_engine("mysql+pymysql://root:Mi911777@localhost:3307/contactsdb")
engine = create_engine("mysql+pymysql://root:Mi911777@localhost:3307/contactsdb")

# sesion para poder hacer transacciones

Session = sessionmaker(bind=engine)
session = Session()

# vinculacion base se encargar de vincular y crear las tablas y mapear
Base = declarative_base()