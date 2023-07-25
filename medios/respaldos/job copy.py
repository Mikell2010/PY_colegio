from flask import render_template, redirect, session, request, flash
from app.models.jobs import Jobs
from app import app

@app.route('/dashboard')
def jobs():

    if 'usuario' not in session:
        return redirect('/login')  
    data = {
        "usuario_id": session['usuario']['usuario_id']  #####
    }  
    trabajos = Jobs.get_all()
    mistrabajos = Jobs.get_all_my_jobs(data)    
    return render_template('jobs/dashboard.html', trabajos=trabajos, mistrabajos=mistrabajos)


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