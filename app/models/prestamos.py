# Python
import os

# Flask
from flask import flash, session

# Conexión a la base de datos
from app.config.mysqlconnection import connectToMySQL


# Variables globales
NOMBRE_MINIMO = 2
def validar(data):
    todo_ok = True
    if len(data['nombres']) < NOMBRE_MINIMO:
        flash("El nombre debe tener al menos 2 caracteres", "danger")
        todo_ok = False
    return todo_ok


class Prestamos:
    """Modelo de la clase Prestamos."""

    def __init__(self, data):
        """Constructor."""

        self.id = data.get('id', 0)
        self.activos_id = data.get('activos_id')
        self.usuario_id = data.get('usuario_id')
        self.admin_entega_id = data.get('admin_entega_id')
        self.admin_recibe_id = data.get('admin_recibe_id')
        self.vigente = data.get('vigente')
        self.observacion = data.get('observacion', '')
        self.fecha_entrega = data.get('fecha_entrega', '')
        self.fecha_recepcion = data.get('fecha_recepcion', '')
        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')

    # SELECCIONA TODOS LOS PRESTAMOS DEL USUARIO LOGEADO
    @classmethod
    def get_all_usuario(cls, data):        
        sql = """
        SELECT *
        FROM prestamos
        WHERE usuario_id = session['usuario']['usuario_id']            
        """        
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)   
    
    # SELECCIONA TODOS LOS PRESTAMOS DEL USUARIO LOGEADO CON DETALLE DEL ACTIVO
    @classmethod
    def get_activos_us_completo(data):
        print ("imprime el data Models prestamos data-id-")
        print(data)    
        id=session['usuario']['usuario_id']
        print(id)

        sql = """
        SELECT *
        FROM activos
        INNER JOIN prestamos ON prestamos.usuario_id = %(id)s
        WHERE activos_id = activos.id AND prestamos.vigente <"3";
        """
        data = {
            'id': id,
        }
        
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
        print(result)
        print("imprimio result")
        return result

    @classmethod
    def save_reserva(cls, data):
        """
        CREA UN NUEVO REGISTRO DE PRESTAMO DEJANDOLO EN MODO DE RESERVA CON USUARIO LOGEADO
        Permite guardar un préstamo en la base de datos.
        """ 
        
        sql = """
        INSERT INTO prestamos (activos_id, usuario_id, vigente, created_at, updated_at)
        VALUES (%(id)s, %(usuario_id)s, '1', NOW(), NOW());
        """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data) 
    
    @classmethod
    def cambio_de_estado_reserva(cls, data):

        sql = """
        UPDATE activos SET
            estado = %(estado)s 
        WHERE id = %(id)s;        
        """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)

    @classmethod
    def save_retiro(cls, data):
        """
        CAMBIA EL ESTADO EN EL REGISTRO DE PRESTAMO DEJANDOLO EN MODO DE ENTREGADO (2) 
        Opcion solo para  ADMINISTRATIVO
        Permite cambiar de estado un préstamo en la base de datos.

        Parámetros:
            - data: contiene el id del activo y el id del usuario.
        """

        sql = """
        UPDATE prestamos SET
            admin_entrega_id = %(usuario_id)s,
            vigente = %(vigente)s,
            observacion = %(observacion)s, 
            fecha_entrega = NOW(),
            updated_at = NOW()
        WHERE activos_id = %(id)s;
        """        
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
    
    @classmethod
    def save_recibe(cls, data):
        """
        MODIFICA EL ESTADO DEL ACTIVO Y AGREGA DATOS AL REGISTRO DEL PRESTAMO,
        AL MOMENTO DE RECIBIR EL ACTIVO.
        Este módulo se ocupa solo para los administrativos.

        Parámetros:
            - data: contiene el id del usuario, estado del activo y el id del
            activo.
        """

        sql = """
        UPDATE prestamos SET
            admin_recibe_id = %(usuario_id)s,
            vigente = %(vigente)s,
            observacion = "sin observacion",
            fecha_recepcion = NOW(),
            updated_at = NOW()
        WHERE activos_id = %(id)s; 
        """        
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
    

    @classmethod
    def save_bloquea(cls, data):
        """
        MODIFICA EL ESTADO Y AGREGA DATOS AL REGISTRO DEL PRÉSTAMO, AL MOMENTO
        DE RECIBIR EL ACTIVO.
        Este módulo se ocupa solo para los administrativos.

        Estados de bloqueo:

            - 0: usuario puede solicitar
            - 3: usuario no puede solictar
        """
        
        sql = """
        UPDATE db_prestamos.usuarios
        SET bloqueo = %(estado)s
        WHERE id = (
            SELECT usuario_id
            FROM db_prestamos.prestamos
            WHERE activos_id = %(id)s
        );
        """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
    

    # MODIFICA EL ESTADO DE UN ALUMNO BLOQUEADO
    # este modulo se ocupa solo para los administrativos
    # bloqueo=0 (usuario puede solicitar)  bloqueo=3 (usuario no puede solictar)
    @classmethod
    def save_desbloquea(cls, data):
        
        sql = """
        UPDATE db_prestamos.usuarios
        SET bloqueo = '0'
        WHERE id = (
            SELECT usuario_id
            FROM db_prestamos.prestamos
            WHERE activos_id = %(id)s
        );
        """
        

        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)


##################################
#    ZONA DE ADMINTRATIVOS       #
##################################

# SELECCIONA TODOS LAS RESERVAS Y PRESTAMOS DEL SISTEMA
# ok!
    @classmethod
    def get_activos_reservados_entregados(cls):   # Recibe data?
        sql = """
        SELECT *
        FROM activos
        INNER JOIN prestamos ON prestamos.activos_id = activos.id
        INNER JOIN usuarios ON prestamos.usuario_id = usuarios.id
        WHERE activos.estado <> 0 AND prestamos.vigente <> 3;
        """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql)         

# SELECCIONA TODOS PRESTAMOS HISTORICOS POR CONTANDO POR MES Y POR FAMILIA EN UN AÑO DEL SISTEMA
# en desarrollo!
    @classmethod
    def get_historico_por_familia(cls,data):   # Recibe data
        
        print(" imprime la anio  ::::::::::::::::::::::::")
        print(data)
        print(f"DATA: %('anio')s")
        
        sql = """
            SELECT 
            EXTRACT(YEAR FROM p.fecha_entrega) AS anio,
            EXTRACT(MONTH FROM p.fecha_entrega) AS mes,
            f.id AS familia_id,
            f.nombre AS nombre_familia,
            COUNT(*) AS cantidad_activos_entregados
            FROM prestamos p
            INNER JOIN activos a ON p.activos_id = a.id
            INNER JOIN familias f ON a.familia_id = f.id
            WHERE EXTRACT(YEAR FROM p.fecha_entrega) = '2023'  
            GROUP BY EXTRACT(YEAR FROM p.fecha_entrega), EXTRACT(MONTH FROM p.fecha_entrega), f.id, f.nombre
            ORDER BY anio, mes, familia_id;
        """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql)         
