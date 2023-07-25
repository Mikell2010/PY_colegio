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
