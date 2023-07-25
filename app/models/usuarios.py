import re
import cv2
import os
from app.config.mysqlconnection import connectToMySQL
from flask import flash

SEGURA_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')

class Usuario:
    def __init__(self, data):
        self.id = data.get('id', 0)
        self.email = data['email'] 
        self.password = data['password']
        self.rut = data.get('rut')
        self.nombres = data.get('nombres')
        self.apellido_p = data.get('apellido_p')
        self.apellido_m = data.get('apellido_m')
        self.curso = data.get('curso')
        self.rol = data.get('rol')
        self.status = data.get('status')
        self.bloqueo = data.get('bloqueo')
        self.es_alumno = data.get('es_alumno')  # El campo puede ser 0 o 5 o 1
        self.fotografia = data.get('fotografia')        
        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')

    @classmethod
    def get_email_sin_seguridad(cls, email):
        print(email)
        print("entro a metodo get sin seguridad")
        sql = """
        SELECT id, email, password, rut, nombres, apellido_p, apellido_m, es_alumno, curso, created_at, updated_at 
        FROM db_prestamos.usuarios where email = %(email)s;
        """
        data = {
            'email': email,
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);     
        print("entro a FOR recorrer metodo get sin seguridad")
        for i in result:
            print(":::valores",result)
            print("salio de for metodo get sin seguridad")
        if result:
            return cls(result[0])

        return None
    

    @classmethod
    def get_password(cls, email):
        sql = """
        SELECT id, email, password, rut, nombres, apellido_p, apellido_m, curso, created_at, updated_at , es_alumno
        FROM usuarios where email = %(email)s and password =rut ;
        """
        data = {
            'email': email,

        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);    
        
        print("entro a FOR recorrerDATA")
        for i in result:
            print(":::valores",data)
            print("salio de for DATA")


        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def get(cls, id):
            sql = """
            SELECT id, email,nombres, rut, apellido,  password, created_at, es_alumno, updated_at FROM usuarios where id = %(id)s;
            """
            data = {
                'id': id
            }
            result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);
            return cls(result[0])

    @classmethod
    def get_by_email(cls, email):
        sql = """
        SELECT id, email, rut, nombres, apellido_p, apellido_m, curso, password,es_alumno, created_at, updated_at FROM usuarios where email = %(email)s and rut = password;
        """
        data = {
            'email': email
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);
        
        print("entro a FOR recorrer metodo get password=rut")
        for i in result:
            print(":::valores",result)
            print("salio de for metodo get get_by_email")
        if result:
            return cls(result[0])

        return None
    
    @classmethod
    def get_usuario(cls, email):
        sql = """
        SELECT id, email, rut, nombres, apellido_p, apellido_m, curso, status, bloqueo,es_alumno, password, created_at, updated_at FROM usuarios where email = %(email)s;
        """
        data = {
            'email': email
        }
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data);

        
        print("entro a FOR recorrer metodo get password=rut")
        for i in result:
            print(":::valores",result)
            print("salio de for metodo get get_USUARIO")
        if result:
            return cls(result[0])

        return None
 
    @staticmethod
    def validar(data):

        todo_ok = True

        if not SEGURA_REGEX.match(data['password']):
            flash("Tu contraseña debe tener 8 caracteres, una mayuscula, minuscula, numero y caracter especial", "danger")
            todo_ok = False

        return todo_ok
    
    @classmethod
    def get_all(cls):
        todos_los_datos = []

        sql = """
        SELECT id, first_name, last_name, email, password, created_at, updated_at,es_alumno FROM usuarios;
        """
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql);
        for fila in result:
            instancia = cls(fila)
            todos_los_datos.append(instancia)
        return todos_los_datos
    
    @classmethod
    def activar_pass(cls, data):
        sql = """
            UPDATE usuarios SET 
            nombres = %(nombres)s,
            apellido_p = %(apellido_p)s,
            apellido_m = %(apellido_m)s,
            es_alumno = %(es_alumno)s,
            curso = %(curso)s,
            email = %(email)s,
            password = %(password)s,
            created_at = NOW(),
            updated_at = NOW()
            WHERE email = %(email)s;
            """
        
        result = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
        return result
    @classmethod
    def save(cls, data):
        sql = f"INSERT INTO usuarios (nombres, apellido_p, apellido_m, curso,email,password ,status,bloqueo,es_alumno,created_at,updated_at) VALUES (%(nombres)s, %(apellido_p)s, %(apellido_m)s,%(curso)s, '1', '1',  %(password)s,NOW(),NOW());"
        id = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
        print("ID:", id)
        resultado = None
        if id:
            resultado = cls.get(id)
        return resultado
    @classmethod
    def saveCRUD(cls, data):
            sql = f"INSERT INTO usuarios (nombres, apellido_p, apellido_m, curso,email,password ,status,bloqueo,es_alumno,created_at,updated_at) VALUES (%(nombres)s, %(apellido_p)s, %(apellido_m)s,%(curso)s, '1', '1',  %(password)s,NOW(),NOW());"
            id = connectToMySQL(os.getenv("BASE_DE_DATOS")).query_db(sql, data)
            print("ID:", id)
            resultado = None
            if id:
                resultado = cls.get(id)
            return resultado

    #################################################################
    #   APARTADO DE VIDEOS Y FOTOGRAFIA                             #
    #################################################################

    @staticmethod
    def foto(data):
        # abrir la cámara
        cap = cv2.VideoCapture(0)

        # establecer dimensiones
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,2560) # ancho
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1440) # alto

        # Tomar una imagen
        ret, frame = cap.read()
        # Guardamos la imagen en un archivo
        cv2.imwrite('C:/Users/Ignacio/Desktop/EXAMEN/app/static/bases/fotos/rostro.jpg',frame)
        #Liberamos la cámara
        cap.release()

        cv2.imshow('Imagen',frame)
        return 

    @staticmethod
    def video(data):
        # abrir la cámara
        captura = cv2.VideoCapture(0) #fuente de captura 0, 1  o 'viedo.avi"        
        salida = cv2.VideoWriter('videoSalida.avi', cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
        
        while(captura.isOpened()):
            ret, frame = captura.read()
            if ret==True:
                cv2.imshow('video',frame)                
                salida.write(frame)           


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
        #frame = cv2.flip(frame,0)  write the flipped frame
        
        # Release everything if job is finished
        salida.release() 
        captura.release()
        cv2.destroyAllWindows()   
        return 

    @staticmethod
    def videfoto(data):
        # abrir la cámara
        captura = cv2.VideoCapture(0) #fuente de captura 0, 1  o 'viedo.avi"
        
        salida = cv2.VideoWriter('videoSalida.avi', cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
        
        while(captura.isOpened()):
            ret, frame = captura.read()
            if ret==True:
                cv2.imshow('video',frame)                
                salida.write(frame) 
                # comienza la foto
                if cv2.waitKey(1) & 0xFF == ord('f'):
                    cap = cv2.VideoCapture(0)

                    # establecer dimensiones
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH,2560) # ancho
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1440) # alto

                    # Tomar una imagen
                    ret, frame = cap.read()
                    # Guardamos la imagen en un archivo
                    cv2.imwrite('C:/Users/Ignacio/Desktop/T_Individual/app/static/bases/fotos/fotoalumno.jpg',frame)
                    #Liberamos la cámara
                    cap.release()

                    break
                
                # termina fotografia
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.imwrite('C:/Users/Ignacio/Desktop/T_Individual/app/static/bases/fotos/fotoalumn1.jpg',frame)


                    break
                
                #frame = cv2.flip(frame,0)
                # write the flipped frame

        # Release everything if job is finished
        salida.release() 
        captura.release()
        cv2.destroyAllWindows()   
        return 


        #cv2.imwrite('C:/Users/Ignacio/Desktop/EXAMEN/app/static/bases/fotos/rostro.jpg',frame)
