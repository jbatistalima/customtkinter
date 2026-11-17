from passlib.hash import bcrypt


# Cria um hash seguro para a senha
def has_password(password: str) -> str:
    return bcrypt.hash(password)

# Verifica hash armazenado
def check_password(password: str, hashed_password: str) -> str:
    return bcrypt.verify(password, hashed_password)