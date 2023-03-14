from app import app
from utils.db import Base, engine
from models import frigorifico
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)