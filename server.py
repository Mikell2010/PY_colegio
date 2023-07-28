from app.controllers import login
from app.controllers import base
from app.controllers import prestamos
from app.controllers import familias

#App config
from app import app
if __name__=="__main__":
    app.run(debug=True)
