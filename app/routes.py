from app import app
from flask import render_template
from .bdcon import *


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')
