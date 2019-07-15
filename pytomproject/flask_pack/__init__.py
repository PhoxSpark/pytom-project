import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import pytom_searcher

app = Flask(__name__)
app.config['SECRET_KEY'] = '58b3c9537fdf0925ad973f2cfb50f48c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
from .pytom_database import Organism, Atom
logging.info("Flask initialized succesfully")