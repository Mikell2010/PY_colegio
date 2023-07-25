import os
from app.config.mysqlconnection import connectToMySQL
from app.models.usuarios import Usuario
from flask import flash, session

NOMBRE_MINIMO = 2

class Jobs:

    def __init__(self, data):
        """Constructor de la clase."""
        
        self.id = data.get('id', 0)
        self.created_by_id = data.get('created_by_id')
        self.asigned_to_id = data.get('asigned_to_id')
        self.title = data.get('title')
        self.location = data.get('location')
        self.description = data.get('description')
        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.usuario = None

    @staticmethod
    def validar(data):

        todo_ok = True
        if len(data['first_name']) < NOMBRE_MINIMO:
            flash("El nombre debe tener al menos 2 caracteres", "danger")
            todo_ok = False
        return todo_ok
    

    @classmethod
    def get_all(cls):        
        sql = """
            SELECT * FROM jobs where jobs.asigned_to_id = '0';            
        """
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql);    
        return result
    

    @classmethod
    def get_all_my_jobs(cls, data):
        
        sql = """
            SELECT * FROM jobs WHERE jobs.asigned_to_id = %(usuario_id)s;            
        """
        # SELECT * FROM jobs JOIN usuarios ON jobs.asigned_to_id = usuarios.id;
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)    
        return result

    @classmethod
    def save(cls, data):
        sql = """
        INSERT INTO jobs (created_by_id, asigned_to_id, title, description, location, created_at, updated_at)
        VALUES (%(usuario_id)s,'0' ,%(title)s, %(description)s, %(location)s, NOW(), NOW());
        """
        id = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
        return

    @classmethod
    def get(cls, id):
        sql = """
        SELECT *
        FROM jobs
        INNER JOIN usuarios
        ON jobs.created_by_id = usuarios.id  WHERE jobs.id = %(id)s;
        """
        data = {
            'id': id
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
        trabajo = cls(result[0])
        return trabajo

    @classmethod
    def delete(cls, id):
        sql = """
        DELETE FROM jobs WHERE id = %(id)s;
        """
        data = {
            'id': id
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);
        return result
    
    @classmethod
    def asigna(cls, id):
        data = {
            'id': id,
            'user_id': session['usuario']['usuario_id'] 
        }

        sql = """
        UPDATE jobs SET asigned_to_id = %(user_id)s WHERE id = %(id)s;
        """        
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);
        return result
    

    @classmethod
    def asigna_job(cls, data):
        sql = """
            UPDATE jobs
                SET
                asigned_to_id = %(usuario_id)s,
                
                updated_at = NOW()
                WHERE id = %(id)s;
            """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)


    @classmethod
    def actualizar(cls, data):

        sql = """
            UPDATE jobs
                SET
                title = %(title)s,
                description = %(description)s,
                location = %(location)s,
                updated_at = NOW()
                WHERE id = %(id)s;
            """
        return connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
    

    @classmethod
    def get_one(cls, id):
        sql = """
        SELECT id, created_by_id, title, description, location, created_at, updated_at FROM jobs WHERE id = %(id)s;
        """
        data = {
            'id': id
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
        # created_by_id: result[0]['created_by_id']        
        datos = cls(result[0])
        return datos

    @classmethod
    def delete(cls, id):
        sql = """
        DELETE FROM jobs WHERE id = %(id)s;
        """
        data = {
            'id': id
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);
        return result
    