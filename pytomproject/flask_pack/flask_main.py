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

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'test' and form.password.data == 'test':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username or password incorrect.', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route('/pytom')
def pytom():
    organism = request.args.get('organism', default = '2ki5', type = str)
    sorted_data = request.args.get('sorted', default = '*', type = str)
    pdb = functions_classes.Object_PDB(organism)
    pdb_data_show = None
    if(sorted_data == 'y'):
        pdb_data_show = pdb.atom_list_sorted
    elif(sorted_data == 'n'):
        pdb_data_show = pdb.atom_list
    else:
        pdb_data_show = pdb.pdb_dictionary

    json = jsonify(pdb_data_show)
    return json
    

app.run(debug=True)