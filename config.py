 # configuracion para coneccion con base de datos para login

class Config:
    # clave secreta para autenticacion en uso de mensajes flash en flask
    SECRET_KEY = 'B!1weNAt1T$%kvhUI*S$'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST='localhost'
    MYSQL_USER= 'root'
    MYSQL_PASSWORD = 'Mi911777'
    MYSQL_DB = 'embarques_db'
    MYSQL_PORT = 3307



config ={
    'development':DevelopmentConfig
}