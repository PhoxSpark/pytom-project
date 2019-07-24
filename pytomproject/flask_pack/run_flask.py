"""
Every flask important function including paths and routes.
"""
import logging
import os
from flask import render_template, request, send_from_directory, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from pytomproject.general_functions import save_obj, load_obj
from .pytom_database import Organism, Atom, add_new_organism
from .pdb_dictionary_statements import PdbDictionaryStatements
from . import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGERIO_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Pytom Project"
    }
)
app.register_blueprint(SWAGGERIO_BLUEPRINT, url_prefix=SWAGGER_URL)

def initial_checks():
    """
    Function that initiates and load data to use on
    pytom functions.
    """
    logging.info("Initializing jsonify and loading data...")
    pdb_dict = PdbDictionaryStatements()
    if os.path.exists("data/" + "dictionary" + ".pkl"):
        pdb_dict = load_obj("dictionary")
    return pdb_dict

def save(pdb_dict):
    """
    Function for save object in to a file.
    """
    logging.info("Saving dictionary...")
    save_obj(pdb_dict, "dictionary")

def organism_loop(group, pdb_dict, organism_selection):
    """
    Loops through the selected organism for transform
    the data on the database to dictionary.
    """
    atom_dict = {}
    for atom in Atom.query.filter_by(organism=group):
        atom = atom.__dict__
        if '_sa_instance_state' in atom:
            del atom['_sa_instance_state']
            if 'id' in atom:
                del atom['id']
                if "ATOM" not in atom_dict:
                    atom_dict[atom["order"]] = atom
                    pdb_dict.pdb_dict[group] = {"ATOM": atom_dict}
                    pdb_dict.organism_list_add(organism_selection)
    return pdb_dict

def organism_split(pdb_dict, organism_selection):
    """
    Split the organism entered by the user and Check
    if it actually exists on the database.
    """
    failed = None
    logging.info("Organism specified, splitting it...")
    organism_selection = organism_selection.split(',')
    for group in organism_selection:
        logging.info("Checking if organism %s exist...", group)
        exists = db.session.query(db.exists().where(Organism.name == group)).scalar()   #pylint: disable=no-member
        logging.info("Organism exists: %s", exists)
        if not exists:
            logging.info("Organism %s not found! It will be created.", group)
            pdb_dict.failed = add_new_organism(group, "Unspecified")
            if not pdb_dict.failed:
                logging.info("Checking if %s exists in dictionary...", group)

                if group not in pdb_dict.pdb_dict:
                    failed = jsonify("Success!")
                    logging.info("%s not found! It will be added in the dictionary.", group)
                    pdb_dict = organism_loop(group, pdb_dict, organism_selection)
                    save(pdb_dict)
                else:
                    logging.info("Organism found.")
                    failed = jsonify("Success!")

        else:
            failed = jsonify("Failed!")
    logging.info("Returning results...")
    return failed

@app.route("/static/<path:path>")
def send_static(path):
    """
    Function for load the static path of Swagger
    """
    return send_from_directory('static', path)

@app.route("/delete")
def delete():
    """
    Reset the dictionary or database. It will reset all
    if there is no parameter.
    """
    pdb_dict = initial_checks()
    failed = None
    logging.info("Reading specified arguments...")
    delete_data = request.args.get("data", default="all", type=str)
    if delete_data in ("all", "database", "dictionary"):
        if delete_data in ("database", "all"):
            logging.info("Renewing database...")
            db.drop_all()
            db.create_all()
            logging.info("Database was renewed.")

        if delete_data in ("dictionary", "all"):
            logging.info("Renewing dictionary...")
            pdb_dict = None
            pdb_dict = PdbDictionaryStatements()
            if os.path.exists("data/" + "dictionary" + ".pkl"):
                os.remove("Data/dictionary.pkl")
        save(pdb_dict)
        logging.info("Operation successful.")
        failed = jsonify("Success!")

    else:
        logging.info("Operation failed.")
        failed = jsonify("Failed!")

    return failed


@app.route("/organism")
def organism():
    """
    Select one or more organisms from a PDB. It requires
    parameters, it don't accept empty.
    """
    pdb_dict = initial_checks()
    failed = None
    logging.info("Reading specified arguments...")
    organism_selection = request.args.get("name", default="*", type=str)
    if organism_selection == "*":
        logging.error("Organism can't be void!")
        logging.info("Operation failed.")
        failed = jsonify("Failed!")

    else:
        failed = organism_split(pdb_dict, organism_selection)
        logging.info("Data returned.")

    return failed

@app.route("/select")
def select():
    """
    Select atoms based on an specified camp or value with
    some different modes.
    """
    select_list = [None, None, None, None]
    pdb_dict = initial_checks()
    failed = None

    logging.info("Reading specified arguments...")
    value = request.args.get("value", default="*", type=str)
    camp = request.args.get("camp", default="*", type=str)
    mode = request.args.get("mode", default="*", type=str)
    organism_selection = request.args.get("organism", default="*", type=str)

    logging.info("Checking if the camps were specified...")

    select_list[0] = value.split(',')
    select_list[1] = camp
    select_list[2] = mode

    if organism_selection == '*':
        organism_selection = pdb_dict.organism_list
        logging.info("Organisms %s saved.", organism_selection)
    else:
        organism_selection = organism_selection.split(',')
        logging.info("Organisms %s saved.", organism_selection)

    logging.info("Arguments added to the list: %s.", select_list)
    logging.info("This have 3 data requirements so every other data will be ignored.")
    logging.info("Proceeding to call the function to apply to PDB object.")

    #NORMAL MODE
    #Normal mode will take an integer and compare it with the specified camp without
    #taking in consideration the decimals. It can take strings or characters but in
    #that case it automatically redirects to the accurate mode.
    if select_list[2] == "normal":
        logging.info("Normal mode recogniced, proceeding...")
        pdb_dict.select_no_accurate(select_list[0], select_list[1])
        save(pdb_dict)
        logging.info("Operation successful.")
        failed = jsonify("Success!")

    #RANGE MODE
    #Takes 2 values integer or float and select all the coincidences between those
    #values. It will sort the values before the function so it doesn't matter where
    #put the max or the min. Also, if the two values are the same aborts the
    #operation and drops a logging error saying that normal or accurate mode can do
    #that (because it has no sense to make a range from 1.5 to 1.5).
    elif select_list[2] == "range":
        logging.info("Range mode recogniced, proceeding...")
        pdb_dict.select_range(select_list[0], select_list[1])
        save(pdb_dict)
        logging.info("Operation successful.")
        failed = jsonify("Success!")

    #ACCURATE MODE
    #Takes an integer or a float and gets the exact coincidence, that simple. It can
    #take list of numbers and organisms like normal mode.
    elif select_list[2] == "accurate":
        logging.info("Accurate mode recogniced, proceeding...")
        pdb_dict.select_camps(select_list[0], select_list[1])
        save(pdb_dict)
        logging.info("Operation successful.")
        failed = jsonify("Success!")

    #NOT RECOGNICED MODE
    else:
        logging.error("The specified mode (%s) is not recogniced.", select_list[2])
        logging.info("Select will not proceed.")
        save(pdb_dict)
        logging.info("Operation failed.")
        failed = jsonify("Failed!")

    return failed

@app.route("/rollback")
def rollback():
    """
    Rollback will go back to the before dictionary.
    """
    pdb_dict = initial_checks()
    pdb_dict.rollback()
    save(pdb_dict)
    logging.info("Operation successful.")
    return jsonify("Success!")

@app.route("/return")
def return_data():
    """
    This URL will return the results of all the querys.
    """
    json_return = None
    pdb_dict = initial_checks()
    pdb_dict.jsonify()
    logging.info("Returning results...")
    if pdb_dict.json is not None:
        json_return = pdb_dict.json
    else:
        logging.info("Operation failed.")
        json_return = jsonify("Failed!")
    return json_return

@app.route("/")
def home():
    """
    Show main page
    """
    return render_template('home.html', title="Pytom")

def start():
    """
    Start flask
    """
    app.run(debug=True)
