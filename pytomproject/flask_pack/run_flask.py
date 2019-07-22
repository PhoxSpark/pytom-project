from .. import general_functions
from . import app, pytom_database, db
from .pdb_dictionary_statements import PDB_Dictionary_Statements
from flask import render_template, url_for, flash, redirect, request, send_from_directory
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

def save():
    #SAVE
    #Default y, it allows the user to decide if he want's to save the on going
    #changes or not.
    pdb_dict = initial_checks()
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
    delete = request.args.get("", default = "all", type = str)
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
        save()
        return(render_template('assertive_response.html', title="Success!"))

    else:
        return(render_template('negative_response.html', title="Error!"))



@app.route("/organism")
def organism():
    """
    Select one or more organisms from a PDB. It requires
    parameters, it don't accept empty.
    """
    pdb_dict = initial_checks()
    logging.info("Reading specified arguments...")
    organism = request.args.get("", default = "*", type = str)
    if(organism == "*"):
        logging.error("Organism can't be void!")
        return(render_template('negative_response.html', title="Error!"))

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
        save()
        return(render_template('assertive_response.html', title="Success!"))


@app.route("/select")
def select():
    """
    Select atoms based on an specified camp or value with
    some different modes.
    """
    select_list = [None, None, None]
    pdb_dict = initial_checks()
    logging.info("Reading specified arguments...")
    select = request.args.get("", default = "all", type = str)
    save()

@app.route("/rollback")
def rollback():
    """
    Rollback will go back to the before dictionary.
    """
    pdb_dict = initial_checks()
    save()

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
        return (render_template('negative_response.html', title="Error!"))


@app.route("/")
def pytom():
    """
    Main tool of Pytom

    You can request an organism and it will be downloaded from the pdb database. The PDB downloaded will 
    be added on the own pytom database, allowing the user to use the PDB's easily even without Internet. 
    The database will translate itself into a Dictionary for easy manipulation from Python.

    Why whould anyone want to manipulate a PDB file? The PDB files are VEY large. This tool can search 
    for atoms (perhaps something more in the future) but if the user want a more concrete search, he can 
    achieve that using arguments on the same URL. Also, with the use of arguments they can decide if the 
    dictionary will save after the consult (for apply more arguments after or take a look without change 
    anything), they can erase the full database (for make space in to the HDD or to start fresh and clean)
    and they can delete all the logs on the dictionary file, so also they can start from zero with a new 
    and empty dictionary.

    All the results will be displayed on json (at the moment). This json will not be sorted and Pytom is 
    not going to bring the tool to sort. I don't have any problem with the philosophy of sorting but the 
    whole pourpose of json is to make it easy to access data to another program or database. A program is 
    not going to care if the json is sorted so it's better to leave it like it is. Also, jsonify sorts a 
    little bit by the first character of the key (or the next if they are equal) to make it prettier to 
    the human eye.

    Arguments: The url has to be like: http://localhost:5000/pytom/? after the ? we start to add arguments 
    and we are going to separate them with & but only if they are from another statement, for example:
    http://localhost:5000/pytom/?organism=2ki5&select=name:CA,N&newdict=y
    Take in consideration that some statements have their own arguments, like select on that example.
    """

    emptydb = request.args.get("newdb", default = '*', type = str)
    emptydict = request.args.get("newdict", default = '*', type = str)
    species = request.args.get("species", default = "Unnspecified", type = str)
    select = request.args.get("select", default = '*', type = str)
    save = request.args.get("save", default = 'y', type = str)
    rollback = request.args.get("rollback", default = '*', type = str)
    
    if(rollback == 'y'):
        logging.info("Trying to rollback to last dictionary...")
        pdb_dict.rollback()
    
    #All the statements goes through this IF
    if(not failed and organism != '*'):
        #SELECT
        #This statement will take the camps you specified and the values and will delete
        #every single row that don't pass the filter.
        if(select != '*'):
            logging.info("Select statement detected, splitting it...")
            select = select.split(';')
            logging.info("Checking if the camps were specified...")
            for values in select:
                if(values.startswith("value:")):
                    select_list[0] = values.replace("value:", '')

                elif(values.startswith("camp:")):
                    select_list[1] = values.replace("camp:", '')

                elif(values.startswith("mode:")):
                    select_list[2] = values.replace("mode:", '')

                else:
                    logging.info("No custom sintax specified.")
                    logging.warning("If you are having problems, don't use custom sintax with default sintax. &select=10;TempFactor;mode:accurate is not equal to &select=10;TempFactor;accurate")
                    select_list = select

            select_list[0] = select_list[0].split(',')
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
                pdb_dict.select_no_accurate(select_list[0], select_list[1], organism)

            #RANGE MODE
            #Takes 2 values integer or float and select all the coincidences between those
            #values. It will sort the values before the function so it doesn't matter where
            #put the max or the min. Also, if the two values are the same aborts the
            #operation and drops a logging error saying that normal or accurate mode can do 
            #that (because it has no sense to make a range from 1.5 to 1.5).
            elif(select_list[2] == "range"):
                logging.info("Range mode recogniced, proceeding...")
                pdb_dict.select_range(select_list[0], select_list[1], organism)

            #ACCURATE MODE
            #Takes an integer or a float and gets the exact coincidence, that simple. It can
            #take list of numbers and organisms like normal mode.
            elif(select_list[2] == "accurate"):
                logging.info("Accurate mode recogniced, proceeding...")
                pdb_dict.select_camps(select_list[0], select_list[1], organism)

            #NOT RECOGNICED MODE
            else:
                logging.error("The specified mode (%s) is not recogniced, select will not proceed." % select_list[2])


    

def start():
    app.run(debug=True)