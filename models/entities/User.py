
# pdw=
# pbkdf2:sha256:600000$CA8QkUU0SBuHrDZS$0a4210c30c891de6b04992481797ba8c4d4f327f691279ceccad48415bbab0ae
# contiene una funcion para comprobar los hash 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

print(check_password_hash('pbkdf2:sha256:600000$4ajuhI2BJJdOyuXx$5e50bacbc96f11c94f30f5169e6cf84689859a9ada63e43cc8920703db0d1902',"Paolo.2023%"))
class User(UserMixin):

    def __init__(self, id, username, password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password  # contraseña en texto plano texto plano
        self.fullname = fullname

    # metodo para comprobar si un password en texto plano coincide con forma hasheada
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)  # retornara true o false
