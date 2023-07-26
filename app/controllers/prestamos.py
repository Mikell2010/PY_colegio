"""Prestamos controllers."""

# App config
from app import app


# Flask
from flask import render_template, redirect, session, request, flash
from mysql.connector import connection, cursor


# Models
from app.models.Borrar_activos import Activo
from app.models.familias import Familia
from app.models.prestamos import Prestamos


@app.route('/dashboard/')
def prestamos():
    """Dashboard."""

    # Proteger ruta "/dashboard/"
    if 'usuario' not in session:
        return redirect('/login')

    data = {
        "usuario_id": session['usuario']['usuario_id']
        }


    # Obtener Activos diponibles (de todas las familias)
    disponibles = Activo.get_activos_disponibles()
    print("##### Disponibles ########")
    print(disponibles)


    # Obtener todas las familias  OK
    familias = Familia.obtener_todas_las_familias()


    # Obtener todas los prestamos activos del usuario   
    mispedidos = Prestamos.get_activos_us_completo()
   
    return render_template(
        'prestamos/dashboard.html',
        disponibles=disponibles,
        familias=familias,
        mispedidos=mispedidos,
    )


@app.route('/buscar_activos_por_familia/')
def buscar_por_fam():
    """desde el Dashboard."""

    # Proteger ruta "/dashboard/"
    if 'usuario' not in session:
        return redirect('/login')

    data = {"familia_id": ('valorSeleccionado')} 
    
    activos = Activo.get_activos_familia_id(data)
    print(activos)

    return render_template(
        'prestamos/dashboard.html',
        familias=activos       
    )


#  busca todos los prestasmo de la tabla prestamos, incluye resrvas
@app.route('/prestamos/')
def buscar_activos_todos_los_activos_en_prestamo():
    # busca los activos en prestamo
    """gestiona."""

    # Proteger ruta "/dashboard/"
    if 'usuario' not in session:
        return redirect('/login')

    #data = {
    #    "familias_id": id
    #} 

    # Obtener todos los activos en prestamo y reservados


    activos_p_r = Prestamos.get_activos_reservados_entregados()
    print(activos_p_r)
    print(" $$$$$$$$$$$ ACTIVOS")
    return render_template(
        'prestamos/gestiona.html',
        activos=activos_p_r,
    
    )

#controladores para Dashboard (ALUMNOS)

@app.route('/prestamos/reservar/', methods=['POST'])
def asignar():
    """Permite realizar un prestamo."""
    
    # Proteger ruta "/prestamos/reservar/"
    if 'usuario' not in session:
        return redirect('/login')
    

    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': request.form['activos_id'],
    }
    data2 = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': request.form['activos_id'],
        'estado' : "1"
    }
    
    Prestamos.save_reserva(data) 
    Prestamos.cambio_de_estado_reserva(data2)
    flash("reservaste con Exito", "success")
    return redirect('/dashboard/')

#controladores para Gestionar (ADMINISTRATIVOS)

@app.route('/prestamos/entregar/<int:id>/')
def entregar(id):
    """Permite actualizar un valor específico de un recurso (entregar un préstamo)."""
  
    # Proteger ruta "/prestamos/entregar/"
    if 'usuario' not in session:
        return redirect('/login')

    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': id,  # Activo
        'vigente': 2,
        'observacion': "Solicitud entregada"
    }

    print(f"DATA: {data}")

    data2 = {
        'id': id,
        'estado': "2"
    }

    Prestamos.save_retiro(data) 
    Prestamos.cambio_de_estado_reserva(data2)

    flash("Registro de Activo entregado con Éxito", "info")
    return redirect("/prestamos/")
#controladores para Gestionar (ADMINISTRATIVOS)

@app.route('/prestamos/eliminar/<int:id>/')
def eliminar(id):
    """Permite actualizar un valor específico de un recurso (entregar un préstamo)."""
  
    # Proteger ruta "/prestamos/eliminar/"
    if 'usuario' not in session:
        return redirect('/login')
    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': id,  # Activo
        'vigente': 3,
        'observacion': "Solicitud eliminada",
    }

    data2 = {
        'id': id,
        'estado': "0",
        
    }

    Prestamos.save_retiro(data) 
    Prestamos.cambio_de_estado_reserva(data2)
  

    flash("Solicitud Eliminada con Éxito", "info")
    return redirect("/prestamos/")


""" controlador que permite devolver un activo prestado
#   recibe desde gestiona.html el valor  prestamos.id 
#   Esto se presenta en la vista de adminsitrativo usuario_es_alunmno= '0' 
#   los alumnos tienen un '1'  la sesion del administrativo 
"""
@app.route('/prestamos/devolver/<int:id>/')
def devolver(id):
    """Permite realizar el Registro de Devolución del Activo."""
            
    # Proteger ruta "/prestamos/devolver/"
    if 'usuario' not in session:
        return redirect('/login')

    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': id,
        'vigente': 3,
        'observacion': "Solicitud Cerrada",
    }
    
    data2 = {
        'id': id,
        'estado' : 0
    }
    Prestamos.save_recibe(data) 
    Activo.cambio_de_estado_reserva(data2)
    flash("Recepcionaste con Exito", "info")
    return redirect('/prestamos/')


""" controlador que permite devolver un activo prestado y bloquear
#   recibe desde gestiona.html el valor  prestamos.id 
#   Esto se presenta en la vista de adminsitrativo usuario_es_alunmno= '0' 
#   los alumnos tienen un '1'  la sesion del administrativo 
"""

@app.route('/prestamos/bloquear/<int:id>/')
def bloquear(id):
    """Permite realizar un prestamo."""

    # Proteger ruta "/prestamos/bloquear/"
    if 'usuario' not in session:
        return redirect('/login')
    #print(request.form[activo.id])

    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': id,
        'vigente': 3,
        'bloqueo': 3,
    }
    data2 = {
        'id': id,
        'estado' : 0
    }
    print(f"DATA: {data}")
    print(f"DATA: {data2}")
    Prestamos.save_recibe(data) 
    Prestamos.save_bloquea(data2) 
    Activo.cambio_de_estado_reserva(data2)
    flash("Recepcionaste con Exito", "info")
    return redirect('/prestamos/')

@app.route('/prestamos/desbloquear/<int:id>/')
def desbloquear(id):
    """Permite realizar un prestamo."""

    # Proteger ruta "/prestamos/bloquear/"
    if 'usuario' not in session:
        return redirect('/login')
    #print(request.form[activo.id])


    data2 = {
        'id': id,
        'estado' : 0
    }

    print(f"DATA: {data2}")

    Prestamos.save_desbloquea(data2) 

    flash("Recepcionaste con Exito", "info")
    return redirect('/prestamos/')


#________________________________________________________________________________________________________________________________
#   ZONA DE CONTROL DE RUTAS PARA ESTADISTICAS
#
#________________________________________________________________________________________________________________________________


#   controlador que permite devolver un activo prestado
#   recibe desde gestiona.html el valor  prestamos.id 
#   Esto se presenta en la vista de adminsitrativo usuario_es_alunmno= '0' 
#   los alumnos tienen un '1'  la sesion del administrativo 

@app.route('/prestamos/asistencia/')
def para_asistencia():
    # "" Permite enviar datos Famila a renderizar a asistencia.html""
            
    # Proteger ruta "/prestamos/asistencia/"
    if 'usuario' not in session:
        return redirect('/login')

    """
    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'tipo_grafico': 1,
        'feha_inicio': '01/01/2023',
        'fecha_termino': '31/12/2023',
        'familia_id' :'1'
    }
    
    data2 = {
        'id': id,
        'estado' : 0
    }
    """
    data = {
        'id': id,
        'nombre': " "
    }
    data = Familia.obtener_todas_las_familias () 
    print(" imprime la data")
    print(f"DATA: {data}")
    flash("Recepcionaste con Exito", "info")
    return render_template('/prestamos/asistencia.html',familias=data)


@app.route('/prestamos/graficar/', methods=['POST'])
def get_chart_data():
    print("metodo form.request")
    print("POST menu: ", request.form)
    data = {
        'id': id,
        'estado' : 0
    }
    return render_template('prestamos/graficoduro2.html',data=data)
    #redirect('prestamos/asistencia')                 

""" 
    # print("cursor = connection.cursor()")

    # Realizar la consulta a la base de datos
    # cursor.execute(
                    """
                   # SELECT * 
    # FROM prestamos
    # WHERE fecha_entrega > '2023-01-01' AND fecha_entrega < '2023-07-22';")
    # """


    # )
""" 
data = [
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    [45, 65, 34, 33, 22, 44, 22 ,33, 44, 55, 32, 66],   # Valores para enero
    [32, 22 ,33, 44, 55, 32, 53, 44, 55, 32, 43, 54],   # Valores para febrero
    [12, 21, 35, 53, 44, 22, 33, 44, 55, 32, 55, 73],
    [45, 65, 34, 33, 22, 44, 22 ,33, 44, 55, 32, 66],
    [32, 22 ,33, 44, 55, 32, 53, 44, 55, 32, 43, 54],  
    [12, 21, 35, 53, 44, 22, 33, 44, 55, 32, 55, 73],
    [45, 65, 34, 33, 22, 44, 22 ,33, 44, 55, 32, 66],
    [34, 65, 34, 54, 22, 44, 28 ,33, 44, 55, 32, 66], 
    [45, 65, 34, 33, 22, 44, 22 ,33, 44, 55, 32, 66],   
    [32, 22 ,33, 44, 55, 32, 53, 44, 55, 32, 43, 54],   
    [12, 21, 35, 53, 44, 22, 33, 44, 55, 32, 55, 73],
    [45, 65, 34, 33, 22, 44, 22 ,33, 44, 55, 32, 66],]

    #@app.route('/graficar',  methods=['POST '], )

    #def get_chart_data():

        
    # data = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    # cursor.close()
    # connection.close()
    data2 = {
        'anio': request.form['anio'],
        'feha_inicio': request.form['feha_inicio'],
        'Fecha_termino': request.form['feha_inicio'],
        'familia': request.form['familia'],
    }
    data3 = {
        'tipo': request.form['tipo']
    }

    # Preparar los datos para el gráfico
    x_values =  Activo.get_historico_por_familia(data2)

    x_values = [row[0] for row in data] # obtiene los meses del año

    largo= len(data) # obtiene el tamaño del arreglo de data, es decir la cantidad de familias que hay, en nuestro caso 3
    y_values = [row[1] for row in data] # obtiene los valores de cada mes 


    # Renderizar el gráfico utilizando una plantilla HTML
return render_template('graficoprueba.html', x_values=x_values, y_values=y_values)
""" 


active_routes = []
for rule in app.url_map.iter_rules():
    active_routes.append(rule)

# Imprimir las rutas activas
for route in active_routes:
    print(route)



""" 
#           /prestamos/entregar
@app.route('/prestamos/entregar/<int:id>/', methods=['GET'])
def entregar():

    print("  ##### llego a Entrega ")   

    # Proteger ruta "/prestamos/entregar/"
    if 'usuario' not in session:
        return redirect('/login')


    data = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': request.form['activos_id'],
    }
    data2 = {
        'usuario_id': session['usuario']['usuario_id'],
        'id': request.form['activos_id'],
        'estado' : "2"
    }
    Prestamos.save_retiro(data) 
    Activo.cambio_de_estado_reserva(data2)
    flash("ERegistro de Activo entregado con Exito", "danger")
    return redirect('/dashboard/')


@app.route('/addJob')
def jobs_crear():
    if 'usuario' not in session:
        return redirect('/login')    
    session['usuario']['first_name']    
    return render_template('jobs/crear.html')


@app.route('/procesar_job', methods=["POST"])
def procesar_job():
    print("DATOS DEL TRABAJO:", request.form)

    data = {
        **request.form,
        "usuario_id": session['usuario']['usuario_id']  #####
    }
    job = Jobs.save(data)
    
    flash(f"Trabajo creado exitosamente", "success")
    return redirect("/")


@app.route('/borrar/<int:id>/', methods=["GET", "POST"])
def borrar(id):
    print(" entro al delete controlador")    
    job = Jobs.delete(id)
    flash(f"Trabajo eliminado exitosamente", "success")
    return redirect("/")


@app.route('/job/view/<int:id>')
def job_id(id):
    if 'usuario' not in session:
        return redirect('/login')
    trabajo = Jobs.get(id)    
    return render_template('jobs/view.html', trabajo=trabajo)


@app.route('/job/asignar/<int:id>')
def asignar(id):
    if 'usuario' not in session:
        return redirect('/login')

    data = {
        "id" : id,
        "usuario_id": session['usuario']['usuario_id']
    }
    trabajo = Jobs.asigna_job(data)    
    return  redirect("/")


@app.route('/edit/<int:id>/', methods=["GET", "POST"])
def editar(id):
    if 'usuario' not in session:
        return redirect('/login')
    datos = Jobs.get_one(id)

    if request.method == "POST":    
        data = {
            'id': id,
            'title' : request.form["title"],
            'description': request.form["description"],
            'location' : request.form["location"],
        }
        Jobs.actualizar(data)
        return redirect("/")

    return  render_template('/jobs/edit.html', datos=datos)
    """