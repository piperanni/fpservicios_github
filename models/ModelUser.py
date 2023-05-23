# metodo que hará la comprobacion de login de usuario
from .entities.User import User
class ModelUser():
    @classmethod
    def login (self,db,user):
        try: # Ejecucion consulta sql
            cursor = db.connection.cursor()
            sql = """SELECT id,username,password,fullname 
            FROM user WHERE username = '{}'""".format(user.username)

            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None: # si no existe el usuario se crea uno nuevo
                user = User(id=row[0],username=row[1],password=User.check_password(row[2],user.password),fullname=row[3])
                return user # retornara el usuario nota: no se le puso un full name, metodo constructor le asigna "" por defecto
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id (self,db,id): # obtener el usuario por id para comprobar la constraseña
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id,username,fullname 
            FROM user WHERE id = '{}'""".format(id)

            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                logged_user = User(row[0],row[1],None,row[2])
                return logged_user # retornara el usuario nota: no se le puso un full name, metodo constructor le asigna "" por defecto
            else:
                return None

        except Exception as ex:
            raise Exception(ex)    