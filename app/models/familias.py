"""Modelo de la clase Familia."""

# Python
import os

# Conexion con la base de datos
from app.config.mysqlconnection import connectToMySQL



class Familia:
    """Clase Familia."""

    def __init__(self, data):
        """Constructor de la clase Familia."""

        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def obtener_todas_las_familias(cls):
        """Obtiene todas las familias de la base de datos."""

        query = """SELECT id, nombre FROM familias;"""
        resultados = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(query)
        return resultados
