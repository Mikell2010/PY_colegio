from flask import render_template, request, redirect, session, flash, jsonify
from app import app
from app.models.usuarios import Usuario
from app.models.prestamos import Prestamos
from flask_bcrypt import Bcrypt
from datetime import timedelta

import cv2


bcrypt = Bcrypt(app) 

@app.route('/login')
def login():

    if 'usuario' in session:
        return redirect('/')
    
    return render_template('auth/login.html')


@app.route('/procesar_login', methods=['POST'])  
def procesar_login():
    print("POST1: ", request.form)    
    usuario_encontrado = Usuario.get_email_sin_seguridad(request.form['email'])

    if not usuario_encontrado:
        flash('No estas en la base de datos, solicita que te ingresen', 'danger')
        return redirect('/login')
    
    # usuario está, pero sin habilitacion, debe cambiar la clave
    consulta_password = Usuario.get_password(request.form['email'])
    
    if consulta_password:
        datos =Usuario.get_by_email(request.form['email'])
        return render_template('auth/crea_usuario.html',datos=datos)
    
    if not consulta_password:
        datos =Usuario.get_usuario(request.form['email'])
        return render_template('auth/login_sistema.html',datos=datos)


@app.route('/ingreso', methods=['POST'])  
def ingreso():    
    print("post del login sistema,request.form")    
    usuario_encontrado =Usuario.get_usuario(request.form['email'])

    login_seguro = bcrypt.check_password_hash(usuario_encontrado.password, request.form['password'])
    if not usuario_encontrado:
        flash('Existe un error en tu correo o contraseña', 'danger')
        return redirect('/')     
    
    print("los datos a l formulario login_sistema")
    print(usuario_encontrado)

    data = {
        "usuario_id": usuario_encontrado.id,
        "nombres": usuario_encontrado.nombres,
        "es_alumno": usuario_encontrado.es_alumno,
        "apellido_p": usuario_encontrado.apellido_p,
        "apellido_m": usuario_encontrado.apellido_m,
        "curso": usuario_encontrado.curso,
        "rol": usuario_encontrado.rol,
        "email": usuario_encontrado.email,       
        "bloqueo" : usuario_encontrado.bloqueo,    
    }

    if login_seguro:
        session['usuario'] = data
        flash('Genial, pudiste entrar sin problemas!!!!', 'success')
        print("paso por loginseguro controlledlogin.py")

    
        admin=session['usuario']['es_alumno']
        
    
        
        if  str(admin) == '0':             # la consulta debe der _ si es_alumno= "5" el cual es el parametro para los administrativos
            return redirect ('/prestamos/')
        if  str(admin) == '10':             # la consulta debe der _ si es_alumno= "5" el cual es el parametro para los administrativos
            #return render_template ('prestamos/asistencia.html/')
            return redirect ('/prestamos/asistencia/')

    else:
        flash('Existe un error en tu correo o contraseña', 'danger')
        return redirect('/login')

    return redirect('/')


@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    print("POST: ", request.form)

    if request.form['password'] != request.form['confirm_password']:
        flash("La contraseña no es igual", "danger")
        return redirect('/login')
    
    if not Usuario.validar(request.form):
        return redirect('/login')

    password_hash = bcrypt.generate_password_hash(request.form['password']) 

    data = {
        'email': request.form['email'],
        'nombres': request.form['nombres'],
        'apellido_p': request.form['apellido_p'],
        'apellido_m': request.form['apellido_m'],
        'curso': request.form['curso'],
        'es_alumno': request.form['es_alumno'],
        'password': password_hash,
        
    }


    # funcionalidad para activar la camara web y captura de fotos
    # desabilita la funcionalidad    
    # foto=Usuario.foto('foto') 

   
    resultado = Usuario.activar_pass(data)
    print("resultados")
    print(resultado)

    if resultado is None:
        flash("Registrado Correctamente", "success")
    else:
        flash("Errores", "danger")

    return redirect('/login')


@app.route('/salir')
def salir():
    session.clear()
    flash('Saliste sin problemas!!!', 'info')
    return redirect('/login')




@app.route('/grafica', methods=['POST'])
def grafica():
    data = request.json
    # Aquí procesas los datos y obtienes la información para mostrar en el modal
    # Por ejemplo, podrías llamar a la función 'foto(data)' de tu modelo
    # y devolver el resultado en formato JSON
    resultado = {
        'titulo': 'Título del Modal',
        'contenido': 'Contenido del modal aquí...'
    }
    return jsonify(resultado)

