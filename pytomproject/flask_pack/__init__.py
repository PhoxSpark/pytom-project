"""
Initialize Flask Package
"""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '58b3c9537fdf0925ad973f2cfb50f48c'
db = SQLAlchemy(app)

from .pytom_database import Organism, Atom
logging.info("Flask initialized succesfully")
