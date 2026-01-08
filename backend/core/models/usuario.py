import bcrypt
from extension import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    contrasena = db.Column(db.String(128), nullable=False)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)

    def set_password(self, password_plano):
        assert password_plano, "La contraseña no puede estar vacía"
        self.contrasena = bcrypt.hashpw(
            password_plano.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def verificar_password(self, password_plano):
        if not self.contrasena:
            return False
        return bcrypt.checkpw(
            password_plano.encode("utf-8"),
            self.contrasena.encode("utf-8")
        )

    
    def cambiar_password(self, password_actual: str, password_nueva: str):
        if not self.verificar_password(password_actual):
            raise Exception("La contraseña actual es incorrecta")

        self.set_password(password_nueva)

    def serialize(self):
        return {
            "id": self.id,
            "mail": self.mail,
            "nombre_usuario": self.nombre_usuario
        }