from app import app
from utils.db import Base, engine
# importacion de modelos para la creacion de las tablas de la base de datos
from models import camion
from models import rampla
from models import conductor
from models import destino
from models import embarque
from models import frigorifico
from models import frontera
from models import status_embarque
from models import transporte

if __name__ == '__main__':
    Base.metadata.create_all(engine) # decimos al programa que cree las bases de datos si no existen
    app.run(debug=True)

    
   
    