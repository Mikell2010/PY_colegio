"""Prestamos controllers."""

# App config
from app import app

# Flask
from flask import render_template, redirect, session, request, flash, canvas


# Models
from app.models.Borrar_activos import Activo
from app.models.familias import Familia

# Conexión a la base de datos
from app.config.mysqlconnection import connectToMySQL

@app.route('/buscar_activos_por_familia/<int:id>')
def busca_activos_por_familia():
    # busca los activos disponibles por familia
    """Dashboard."""

    # Proteger ruta "/dashboard/"
    if 'usuario' not in session:
        return redirect('/login')

    data = {
        "familias_id": id
    } 
   
    # Obtener todos los activos disponibles
    activos_familia_disponibles = Activo.get_activos_disponibles_por_familia_id(data)
    
    return render_template(
        'prestamos/dashboard.html',
        activos=activos_familia_disponibles,
    
    )



@app.route('/devolver/')
def devolver():

    # Proteger ruta "/devolver/"
    if 'usuario' not in session:
        return redirect('/login')  
    data = {
        "usuario_id": session['usuario']['usuario_id'] 
    } 
    print("muestra data") 
    print(data)
   
    #activos= Activo(None)
    #disponible = activos.get_disponibles()
    #mispedidos = Prestamos.get_all_usuario(data) , mispedidos=mispedidos return render_template('dashboard.html', disponible=disponible)

    return render_template('prestamos/dashboard.html')


@app.route('/bloquear/')
def bloquear():

    # Proteger ruta "/bloquear/"
    if 'usuario' not in session:
        return redirect('/login')  
    data = {
        "usuario_id": session['usuario']['usuario_id'] 
    } 
    print("muestra data") 
    print(data)
   
    #activos= Activo(None)
    #disponible = activos.get_disponibles()
    #mispedidos = Prestamos.get_all_usuario(data) , mispedidos=mispedidos return render_template('dashboard.html', disponible=disponible)

    return render_template('prestamos/dashboard.html')

# CAMBIA EL ESTADO A LOS ACTIVOS DEVOLUCION/ENTREGA/RESERVA , 
    # estatus=0 (dispnible), estatus= 1 (reservado), estatus=2(prestado)





