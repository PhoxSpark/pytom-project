from .. import general_functions
from . import app, pytom_database, db
from .pdb_dictionary_statements import PDB_Dictionary_Statements
from flask import render_template, url_for, flash, redirect, request, send_from_directory, jsonify
from .pytom_database import Organism, Atom, add_new_organism
from flask_swagger_ui import get_swaggerui_blueprint
import logging, os

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swaggerio_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Pytom Project"
    }
)
app.register_blueprint(swaggerio_blueprint, url_prefix=SWAGGER_URL)

def initial_checks():
    logging.info("Initializing jsonify and loading data...")
    pdb_dict = PDB_Dictionary_Statements()
    if(os.path.exists("data/" + "dictionary" + ".pkl")):
        pdb_dict = general_functions.load_obj("dictionary")
    return pdb_dict

def save(pdb_dict):
    logging.info("Saving dictionary...")
    general_functions.save_obj(pdb_dict, "dictionary")

@app.route("/static/<path:path>")
def send_static(path):
    """
    """
    return send_from_directory('static', path)

@app.route("/delete")
def delete():
    """
    Reset the dictionary or database. It will reset all
    if there is no parameter.
    """
    failed = None
    pdb_dict = initial_checks()
    logging.info("Reading specified arguments...")
    delete = request.args.get("data", default = "all", type = str)
    if(delete == "all" or delete == "database" or delete == "dictionary"):
        if(delete == "database" or delete == "all"):
            logging.info("Renewing database...")
            db.drop_all()
            db.create_all()
            logging.info("Database was renewed.")

        if(delete == "dictionary" or delete == "all"):
            logging.info("Renewing dictionary...")
            pdb_dict = None
            pdb_dict = PDB_Dictionary_Statements()
            os.remove("Data/dictionary.pkl")
        save(pdb_dict)
        logging.info("Operation successful.")
        return jsonify("Success!")

    else:
        logging.info("Operation failed.")
        return jsonify("Failed!")



@app.route("/organism")
def organism():
    """
    Select one or more organisms from a PDB. It requires
    parameters, it don't accept empty.
    """
    pdb_dict = initial_checks()
    logging.info("Reading specified arguments...")
    organism = request.args.get("name", default = "*", type = str)
    if(organism == "*"):
        logging.error("Organism can't be void!")
        logging.info("Operation failed.")
        return jsonify("Failed!")

    else:
        logging.info("Organism specified, splitting it...")
        organism = organism.split(',')
        for group in organism:
            logging.info("Checking if organism %s exist..." % group)
            exists = db.session.query(db.exists().where(Organism.name == group)).scalar()           #pylint: disable=no-member

            if(not exists):
                logging.info("Organism %s not found! It will be created." % group)
                pdb_dict.failed = add_new_organism(group, "Unspecified")

            if(not pdb_dict.failed):
                logging.info("Checking if %s exists in dictionary..." % group)

                if(group not in pdb_dict.pdb_dict):
                    logging.info("%s not found! It will be added in the dictionary for future use and manipulation..." % group)
                    atom_dict = {}

                    for atom in Atom.query.filter_by(organism = group):                             #pylint: disable=no-member
                        atom = atom.__dict__
                        if '_sa_instance_state' in atom: del atom['_sa_instance_state']
                        if 'id' in atom: del atom['id']
                        if("ATOM" not in atom_dict):
                            atom_dict[atom["order"]] = atom

                    pdb_dict.pdb_dict[group] = {"ATOM": atom_dict}
        pdb_dict.organism_list_add(organism)
        logging.info("Organisms %s added to list." % pdb_dict.organism_list)
        save(pdb_dict)
        logging.info("Operation successful.")
        return jsonify("Success!")


@app.route("/select")
def select():
    """
    Select atoms based on an specified camp or value with
    some different modes.
    """
    select_list = [None, None, None, None]
    pdb_dict = initial_checks()

    logging.info("Reading specified arguments...")
    value = request.args.get("value", default = "*", type = str)
    camp = request.args.get("camp", default = "*", type = str)
    mode = request.args.get("mode", default = "*", type = str)
    organism = request.args.get("organism", default = "*", type = str)

    logging.info("Checking if the camps were specified...")

    select_list[0] = value.split(',')
    select_list[1] = camp
    select_list[2] = mode

    if(organism == '*'):
        organism = pdb_dict.organism_list
        logging.info("Organisms %s saved." % organism)
    else:
        organism = organism.split(',')
        logging.info("Organisms %s saved." % organism)

    for i, selection in enumerate(select_list[0]):

        try:
            logging.info("Determining if %s is a string and can be transformed in to a float." % selection)
            float(selection)
        except:
            logging.warning("The data is a string or a character and can't be transformed in to a float.")
        else:
            logging.info("The data now is transformed in to float.")
            select_list[0][i] = float(selection)

    logging.info("Arguments added to the list: %s, this have 3 data requirements so every other data will be ignored. Proceeding to call the function to apply to PDB object." % select_list)

    #NORMAL MODE
    #Normal mode will take an integer and compare it with the specified camp without
    #taking in consideration the decimals. It can take strings or characters but in
    #that case it automatically redirects to the accurate mode.
    if(select_list[2] == "normal"):
        logging.info("Normal mode recogniced, proceeding...")
        pdb_dict.select_no_accurate(select_list[0], select_list[1])
        save(pdb_dict)
        logging.info("Operation successful.")
        return jsonify("Success!")

    #RANGE MODE
    #Takes 2 values integer or float and select all the coincidences between those
    #values. It will sort the values before the function so it doesn't matter where
    #put the max or the min. Also, if the two values are the same aborts the
    #operation and drops a logging error saying that normal or accurate mode can do
    #that (because it has no sense to make a range from 1.5 to 1.5).
    elif(select_list[2] == "range"):
        logging.info("Range mode recogniced, proceeding...")
        pdb_dict.select_range(select_list[0], select_list[1])
        save(pdb_dict)
        logging.info("Operation successful.")
        return jsonify("Success!")

    #ACCURATE MODE
    #Takes an integer or a float and gets the exact coincidence, that simple. It can
    #take list of numbers and organisms like normal mode.
    elif(select_list[2] == "accurate"):
        logging.info("Accurate mode recogniced, proceeding...")
        pdb_dict.select_camps(select_list[0], select_list[1])
        save(pdb_dict)
        logging.info("Operation successful.")
        return jsonify("Success!")

    #NOT RECOGNICED MODE
    else:
        logging.error("The specified mode (%s) is not recogniced, select will not proceed." % select_list[2])
        save(pdb_dict)
        logging.info("Operation failed.")
        return jsonify("Failed!")

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
    pdb_dict = initial_checks()
    pdb_dict.jsonify()
    logging.info("Returning results...")
    if(pdb_dict.json != None):
        return pdb_dict.json
    else:
        logging.info("Operation failed.")
        return jsonify("Failed!")

@app.route("/")
def home():
    """
    Show main page
    """
    return render_template('home.html', title="Pytom")

def start():
    app.run(debug=True)
