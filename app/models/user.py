from peewee import Model, CharField, DateTimeField
from datetime import datetime
from app.models import db 
from passlib.hash import sha256_crypt   


# Modelo base
class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    full_name = CharField(max_length=255)
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=100, unique=True)
    contact = CharField(max_length=20, null=True)
    position = CharField(max_length=100, null=True)
    password_hash = CharField(max_length=255)
    role = CharField(max_length=20, default='user') # admin / user
    created_at = DateTimeField(default=datetime.now)


    # Cadastrar novo usuário
    def set_password(self, password: str):
        self.password_hash = sha256_crypt.hash(password)


    # Verificar autencidade de senha
    def verify_password(self, password: str) -> bool:
        return sha256_crypt.verify(password, self.password_hash)


    def __str__(self):
        return f"{self.username}"
        #return f"{self.full_name}"  # {self.username} - {self.role}"
