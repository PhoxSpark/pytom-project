import sys, logging, os, shutil
sys.path.append("..")
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from pytomproject.flask_pack.forms import RegistrationForm, LoginForm
import pytomproject.functions_classes as functions_classes

#-----------------Log block-------------------
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO)
#---------------------------------------------

app = Flask(__name__)
logging.info("Flask initialized succesfully")

"""
This module will load every Flask related webapp stuff. After
being load, it will show the localhost direction for open and
interactuate with it.
"""

app.config['SECRET_KEY'] = '58b3c9537fdf0925ad973f2cfb50f48c'

@app.route("/")
@app.route("/home")
def home():
    """
    Load the home page when request from / or /home.
    """
    logging.info("Loading home page.")
    return render_template('home.html', title="Home")

@app.route("/pytom")
def pytom():
    """
    Load the pytom page with instructions of use.
    It can have some forms for automation and more user
    friendly GUI.
    """
    logging.info("Loading pytom page.")
    return render_template('pytom.html', title="Pytom Tool")

@app.route("/pytom/")
def pytom_jsonify():
    """
    Used to request the json file, it can accept parameters
    to make a custom json file. All the parameters make
    modifications in to the atom_list atribute from the
    PDB class. The changes will execute in the order of
    this function, not from left to right!
    """
    logging.info("Starting Pytom Jsonify.")
    pdb_dict = {}

    #There is some arguments
    organism = request.args.get('organism', default = '2ki5', type = str)
    erase_files = request.args.get('eraseall', default = '*', type = str)
    erase_file = request.args.get('erase', default = '*', type = str)

    #Detect if user wants to erase files or use existing ones.
    logging.info("Starting Pytom Jsonify")
    if(erase_files != '*' or erase_file != '*'):
        logging.info("Detected erase petition")
        if(erase_files != '*' and erase_file != '*'):
            logging.error("Can't erase all files and a single file! Choose only one option of that kind")
        else:
            if(erase_files != '*'):
                logging.info("Deleting Pytom Downloads folder")
                try:
                    shutil.rmtree("Pytom_Downloads")
                except FileNotFoundError:
                    logging.error("Folder not found")
                    flash("Error! Folder not found. Probably it wasn't been made it. The folder will be created automatically when you make the first consult.", category='danger')
                else:
                    logging.info("Folder removed successfuly")
                    flash('Success! Folder deleted!', category='success')
            if(erase_file != '*'):
                logging.info("Deleting specified PDB")
                try:
                    os.remove(pdb_dict[erase_file].path + pdb_dict[erase_file].name)
                except KeyError:
                    logging.error("File not found")
                    flash("Error! File not found. Probably it wasn't been downloaded. Use ?organism=(organism) to download one. If you leave all blank it will download an example organism (2ki5).", category='danger')
                else:
                    logging.info("File removed successfuly")
                    flash('Success! File deleted!', category='success')
    else:
        logging.info("Creating new object PDB")
        pdb_dict[organism] = functions_classes.Object_PDB(organism)

    #There is the rest of arguments.
    sorted_data = request.args.get('sorted', default = '*', type = str)
    atom_name = request.args.get('atom', default = '*', type = str)
    element = request.args.get('element', default = '*', type = str)
    chainid = request.args.get('chainid', default = '*', type = str)
    occupancy = request.args.get('occupancy', default = None, type = float)
    order = request.args.get('order', default = None, type = int)
    resname = request.args.get('resname', default = '*', type = str)
    serial = request.args.get('serial', default = None, type = int)
    order_min = request.args.get('ordmin', default = None, type = int)
    order_max = request.args.get('ordmax', default = None, type = int)
    temp_factor = request.args.get('tempfact', default = None, type = int)
    temp_factor_accurate = request.args.get('tempfactacc', default = None, type = float)
    temp_factor_range_min = request.args.get('tempfactmin', default = None, type = float)
    temp_factor_range_max = request.args.get('tempfactmax', default = None, type = float)
    x = request.args.get('x', default = None, type = int)
    y = request.args.get('y', default = None, type = int)
    z = request.args.get('z', default = None, type = int)
    x_accurate = request.args.get('xacc', default = None, type = float)
    y_accurate = request.args.get('yacc', default = None, type = float)
    z_accurate = request.args.get('zacc', default = None, type = float)
    x_range_min = request.args.get('xmin', default = None, type = float)
    y_range_min = request.args.get('ymin', default = None, type = float)
    z_range_min = request.args.get('zmin', default = None, type = float)
    x_range_max = request.args.get('xmax', default = None, type = float)
    y_range_max = request.args.get('ymax', default = None, type = float)
    z_range_max = request.args.get('zmax', default = None, type = float)

    #Detect sort input
    logging.info("Starting reading input")
    if(sorted_data == 'y'):
        logging.info("Sort data detected, executing sorted function")
        pass

    #Detect atom name input
    if(atom_name != '*'):
        logging.info("Atom name specified, aplying to object")
        pdb_dict[organism].select_camps(atom_name, "Name")

    #Detect element input
    if(element != '*'):
        logging.info("Element specified, aplying to object")
        pdb_dict[organism].select_camps(element, "ElementSymbol")
    
    #Detect chain ID input
    if(chainid != '*'):
        logging.info("ChainID specified, aplying to object")
        pdb_dict[organism].select_camps(chainid, "ChainID")
    
    #Detect occupancy input
    if(occupancy != None):
        logging.info("Occupancy specified, aplying to object")
        pdb_dict[organism].select_camps(occupancy, "Occupancy")
    
    #Detect order input
    if(order != None):
        logging.info("Order specified, aplying to object")
        pdb_dict[organism].select_camps(order, "Order")

    #Detect resname input
    if(resname != '*'):
        logging.info("Residue name specified, aplying to object")
        pdb_dict[organism].select_camps(resname, "ResName")

    #Detect serial input
    if(serial != None):
        logging.info("Serial specified, aplying to object")
        pdb_dict[organism].select_camps(serial, "Serial")

    #Detect order range input
    if(order_min != None or order_max != None):
        logging.info("Detected range of order, minimum and maximum will be specified")
        minimum, maximum = pdb_dict[organism].set_max_and_mins(order_min, order_max)
        logging.info("Minimum and maximum aparently specified, continuing aplying to object")
        pdb_dict[organism].select_range(minimum, maximum, "Order")

    #Detect temp factor accurate input
    if(temp_factor_accurate != None):
        logging.info("Temperature factor accurate specified, aplying to object")
        pdb_dict[organism].select_camps(temp_factor_accurate, "TempFactor")


    if(temp_factor_range_min != None or temp_factor_range_max != None):
        logging.info("Detected range of temperature factor range, minimum and maximum will be specified")
        minimum, maximum = pdb_dict[organism].set_max_and_mins(temp_factor_range_min, temp_factor_range_max)
        logging.info("Minimum and maximum aparently specified, continuing aplying to object")
        pdb_dict[organism].select_range(minimum, maximum, "TempFactor")

    if(x_accurate != None):
        logging.info("X accurated specified, aplying to object")
        pdb_dict[organism].select_camps(x_accurate, "X")
    
    if(y_accurate != None):
        logging.info("Y accurated specified, aplying to object")
        pdb_dict[organism].select_camps(y_accurate, "Y")
    
    if(z_accurate != None):
        logging.info("Z accurated specified, aplying to object")
        pdb_dict[organism].select_camps(z_accurate, "Z")

    if(x_range_min != None or x_range_max != None):
        logging.info("Detected range X, minimum and maximum will be specified")
        minimum, maximum = pdb_dict[organism].set_max_and_mins(x_range_min, x_range_max)
        logging.info("Minimum and maximum aparently specified, continuing aplying to object")
        pdb_dict[organism].select_range(minimum, maximum, "X")
    
    if(y_range_min != None or y_range_max != None):
        logging.info("Detected range Y, minimum and maximum will be specified")
        minimum, maximum = pdb_dict[organism].set_max_and_mins(y_range_min, y_range_max)
        logging.info("Minimum and maximum aparently specified, continuing aplying to object")
        pdb_dict[organism].select_range(minimum, maximum, "Y")
    
    if(z_range_min != None or z_range_max != None):
        logging.info("Detected range Z, minimum and maximum will be specified")
        minimum, maximum = pdb_dict[organism].set_max_and_mins(z_range_min, z_range_max)
        logging.info("Minimum and maximum aparently specified, continuing aplying to object")
        pdb_dict[organism].select_range(minimum, maximum, "Z")

    json = None

    if(erase_file != '*' or erase_files != '*'):
        json = render_template('pytom.html', title="Pytom Tool")
    else:    
        json = jsonify(pdb_dict[organism].atom_list)

    return json
    
def run_flask():
    app.run(debug=True)