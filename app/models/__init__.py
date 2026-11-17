from peewee import  SqliteDatabase


# Banco de dados
db = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})