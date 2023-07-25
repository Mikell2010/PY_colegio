# App config
from app import app

# Controllers
from app.controllers import login
from app.controllers import base
from app.controllers import prestamos


if __name__=="__main__":
    app.run(debug=True)   