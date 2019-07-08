import sys
sys.path.append("..")
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from pytomproject.flask_pack.forms import RegistrationForm, LoginForm
import pytomproject.functions_classes as functions_classes

app = Flask(__name__)

"""
This module will load every Flask related webapp stuff. After
being load, it will show the localhost direction for open and
interactuate with it.
"""

app.config['SECRET_KEY'] = '58b3c9537fdf0925ad973f2cfb50f48c'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Home")

@app.route("/pytom")
def pytom():
    return render_template('pytom.html', title="Pytom Tool")

@app.route("/pytom/jsonify")
def pytom_jsonify():
    organism = request.args.get('organism', default = '2ki5', type = str)
    sorted_data = request.args.get('sorted', default = '*', type = str)
    atom_name = request.args.get('atom', default = '*', type = str)
    
    pdb = functions_classes.Object_PDB(organism)

    if(atom_name != '*'):
        pdb.make_atom_list_atom(atom_name)

    
    json = jsonify(pdb.atom_list)
    return json
    

app.run(debug=True)