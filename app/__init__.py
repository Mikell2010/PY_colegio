import os
import colorama


from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)


load_dotenv()

app.secret_key = os.getenv("LLAVE_SECRETA")
