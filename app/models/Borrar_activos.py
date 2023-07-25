import os

# Conexión a la base de datos
from app.config.mysqlconnection import connectToMySQL

# from app.models.usuarios import Usuario
# from app.models.prestamos import Prestamos

# from flask import flash, session



#------------------------------------------------
# sección con los modelos de ACTIVOS            #
#------------------------------------------------
class Activo:
    def __init__(self, data):
        """Constructor de la clase."""

        self.id= data.get('id')
        self.codigo= data.get('codigo')
        self.nombre = data.get('nombre')
        self.modelo = data.get('modelo')
        self.operativo = data.get('operativo')
        self.estado = data.get('estado')
        self.familia_id = data.get('familia_id', '')
        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')
 
    # FILTRA LOS ACTIVOS DISPONIBLES POR FAMILIA
    @classmethod
    def get_activos_disponibles(self):
        """Obtener todos los activos disponibles """ 
        """ cambia el valor de 0 a 1 a bandera para quemiestre el  select de famila"""
        # bandera="1"
        query = """
        SELECT activos.*
        FROM activos
        WHERE activos.estado = 0 ;    
        """
        resultados = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(query)
        return resultados
    
     # FILTRA LOS ACTIVOS DISPONIBLE POR FAMILIA CO
    @classmethod
    def get_activos_disponibles_por_familia_id(self):
        """Obtener todos los activos disponibles por familia"""

        query = """
        SELECT activos.*
        FROM activos
        WHERE activos.estado = 0;    
        """
        resultados = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(query)
        return resultados
    

    
    # CAMBIA EL ESTADO A LOS ACTIVOS DEVOLUCION/ENTREGA/RESERVA , 
    # estatus=0 (dispnible), estatus= 1 (reservado), estatus=2(prestado)

    @classmethod
    def cambio_de_estado_reserva(cls, data):
        sql = """
        UPDATE activos SET
            estado = %(estado)s       
        WHERE id = %(id)s;        
        """
        print("metodo de clase::: CAMBIO_DE_ESTADO")
        #Activos.result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql1, estado)
        
        print(" imprime trabajo")   
        
        return  connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)

