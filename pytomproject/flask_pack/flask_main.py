import logging, os, shutil
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from . import pytom_searcher

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
    logging.info("Loading home page...")
    return render_template('home.html', title="Home")

@app.route("/pytom")
def pytom():
    """
    Load the pytom page with instructions of use.
    It can have some forms for automation and more user
    friendly GUI.
    """
    logging.info("Loading pytom page...")
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
    logging.info("Starting Pytom Jsonify...")
    pdb_dict = {}

    #There is some arguments
    organism = request.args.get('organism', default = '2ki5', type = str)
    erase_files = request.args.get('eraseall', default = '*', type = str)
    erase_file = request.args.get('erase', default = '*', type = str)

    #Detect if user wants to erase files or use existing ones.
    logging.info("Trying to detect if user wants to delete...")
    if(erase_files != '*' or erase_file != '*'):
        logging.info("Detected erase petition!")
        if(erase_files != '*' and erase_file != '*'):
            logging.error("Can't erase all files and a single file! Choose only one option of that kind.")
        else:
            if(erase_files != '*'):
                logging.info("Deleting Pytom Downloads folder...")
                try:
                    shutil.rmtree("Pytom_Downloads")
                except FileNotFoundError:
                    logging.error("Folder not found!")
                    flash("Error! Folder not found. Probably it wasn't been made it. The folder will be created automatically when you make the first consult.", category='danger')
                else:
                    logging.info("Folder removed successfuly!")
                    flash('Success! Folder deleted!', category='success')
            if(erase_file != '*'):
                logging.info("Deleting specified PDB...")
                try:
                    os.remove(pdb_dict[erase_file].path + pdb_dict[erase_file].name)
                except KeyError:
                    logging.error("File not found!")
                    flash("Error! File not found. Probably it wasn't been downloaded. Use ?organism=(organism) to download one. If you leave all blank it will download an example organism (2ki5).", category='danger')
                else:
                    logging.info("File removed successfuly!")
                    flash('Success! File deleted!', category='success')
    else:
        logging.info("Creating new object PDB...")
        pdb_dict[organism] = pytom_searcher.Object_PDB(organism)
        if(pdb_dict[organism].invalid):
            logging.error("Program can't continue, probably due to a bad organism name.")
            flash('Error downloading PDB, make sure you writed the organism name correctly or you have internet access.', category='danger')
            erase_file = 'y'

        else:

            logging.info("Organism specified, reading arguments...")

            #Select statement
            select = request.args.get('select', default = "*", type = str)
            pdb_dict[organism].select_function(select, organism)
            
            # Sort statement
            
            
    #Applying in the return
    logging.info("Applying changes to the return variable...")
    logging.info("Clearing json variable...")
    json = None

    logging.info("Determining if a redirect is necessary...")
    if(erase_file != '*' or erase_files != '*'):
        logging.info("Nothing to display, redirection will proceed.")
        json = render_template('pytom.html', title="Pytom Tool")
    else:
        logging.info("ATOM Data will be displayed.")
        json = jsonify(pdb_dict[organism].atom_list)

    logging.info("Returning results...")
    return json
    
def run_flask():
    app.run(debug=True)