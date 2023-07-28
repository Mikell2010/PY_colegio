from flask import render_template, redirect, session, flash as flask
from flask_mail import Mail, Message

from app import app

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'fc8c9cc96bb4f7'
app.config['MAIL_PASSWORD'] = '60b6af13965e27'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = "mschocken@gmail.com"


mail = Mail(app)



@app.route('/')
def inicio():
    return redirect('/dashboard')

@app.route('/enviar_mail')
def enviar_mail():

    # Enviar correo
    msg = Message(
        "Sugerencias, Reclamos y Felicitaciones",
        #sender="mschocken@gmail.com",
        recipients=["mail@mail.com"]#"fernando.ojeda@sip.cl"
        )

    # Renderiza la plantilla HTML con los datos necesarios
    html_body = render_template('auth/correo.html')

    msg.body = "Esto es una prueba de correo testing"
    msg.html = html_body

    with app.open_resource("img/unnamed.png") as fp:
        msg.attach("unnamed.png", "image/png", fp.read())

    try:
      
        print(mail.send(msg))
        flask('TU SOLICITUD DE CORREO HA SIDO ENVIADA, PRONTO TE CONTACTARÁN...', 'success')
    except:
        flask("Error al enviar correo", "danger")


    return redirect('/login')
