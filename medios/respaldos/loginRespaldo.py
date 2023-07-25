from flask import render_template, request, redirect, session, flash
from app.models.usuarios import Usuario
from app import app
from flask_bcrypt import Bcrypt
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
        usuario_encontrado =Usuario.get_usuario(request.form['email'])
        login_seguro = bcrypt.check_password_hash(usuario_encontrado.password, consulta_password.password)
        print("los datos a l formulario login_sistema")
        print(usuario_encontrado)

    data = {
        "usuario_id": usuario_encontrado.id,
        "nombres": usuario_encontrado.nombres,
        "apellido_p": usuario_encontrado.apellido_p,
        "apellido_p": usuario_encontrado.apellido_m,
        "curso": usuario_encontrado.curso,
        "email": usuario_encontrado.email,
    }

    if login_seguro:
        session['usuario'] = data
        flash('Genial, pudiste entrar sin problemas!!!!', 'success')

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
        'password': password_hash,
        
    }

    #existe_usuario = Usuario.get_by_email(request.form['email']) #, methods=["GET"])

    
    #foto=Usuario.videofoto('foto') 

   
    resultado = Usuario.activar_pass(data)
    print("resultasosss")
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

