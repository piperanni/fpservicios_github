from flask import Flask
from routes.frigorificos import frigorificos

app = Flask(__name__)
app.register_blueprint(frigorificos) # perfecto permite llamar a las rutas almacenadas en utils para eso sirve
 


