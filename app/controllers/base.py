from flask import render_template, redirect, session

from app import app


@app.route('/')
def inicio():
    return redirect('/dashboard')