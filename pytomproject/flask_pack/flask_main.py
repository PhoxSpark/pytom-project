import logging, os, shutil
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from . import forms
from .. import functions_classes

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
        pdb_dict[organism] = functions_classes.Object_PDB(organism)
        if(pdb_dict[organism].invalid):
            logging.error("Program can't continue, probably due to a bad organism name.")
            flash('Error downloading PDB, make sure you writed the organism name correctly or you have internet access.', category='danger')
            erase_file = 'y'

        else:

            logging.info("Organism specified, reading arguments...")

            ##There is the rest of arguments.
                
            # Select argument.
            # Additional atributes can be added with ;
            # Some atributes can have multiple values, this will be separed with ,
            # By default, this is the order of the atributes:
            # &select=value;camp;mode
            # The camps can be specified writing the camp name and : like value:
            select = request.args.get('select', default = "*", type = str)
            select = select.split(';')
            select_list = [None, None, None]
            for values in select:
                if(values.startswith("value:")):
                    select_list[0] = values.replace("value:", '')

                elif(values.startswith("camp:")):
                    select_list[1] = values.replace("camp:", '')

                elif(values.startswith("mode:")):
                    select_list[2] = values.replace("mode:", '')

                else:
                    select_list = select

            select_list[0] = select_list[0].split(',')
            
            logging.info("Arguments added to the list: %s, this have 3 data requirements so every other data will be ignored. Proceeding to call the function to apply to PDB object." % select_list)
            
            if(select_list[2] == "normal"):
                logging.info("Normal mode recogniced, proceeding...")

            elif(select_list[2] == "range"):
                logging.info("Range mode recogniced, looking for two values...")

                if(len(select_list[0]) == 2):
                    logging.info("Found two values, are the same?")

                    if(select_list[0][0] != select_list[0][1]):
                        logging.info("The values %s aren't equal, sorting..." % select_list[0])
                        select_list[0] = sorted(select_list[0])
                        logging.info("The values are now sorted, calling function to apply range on the PDB...")
                        pdb_dict[organism].select_range(select_list[0][0], select_list[0][1], select_list[1])
                        logging.info("Range applyied.")

                    else:
                        logging.error("The values are equal, try with normal mode.")

                else:
                    logging.error("Wrong number of values, expected 2.")
                    

            elif(select_list[2] == "accurate"):
                logging.info("Accurate mode recogniced, proceeding...")
                pdb_dict[organism].select_camps(select_list[0], select_list[1])
                
            else:
                logging.error("The specified mode (%s) is not recogniced, select will not proceed." % select_list[2])
            
            # Sort argument.

            

            """
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

            logging.info("Starting reading input...")

            #Detect sort input
            if(sorted_data == 'y'):
                logging.info("Sort data detected, executing sorted function...")
                pass

            #Detect atom name input
            if(atom_name != '*'):
                logging.info("Atom name specified, aplying to object...")
                pdb_dict[organism].select_camps(atom_name, "Name")

            #Detect element input
            if(element != '*'):
                logging.info("Element specified, aplying to object...")
                pdb_dict[organism].select_camps(element, "ElementSymbol")
            
            #Detect chain ID input
            if(chainid != '*'):
                logging.info("ChainID specified, aplying to object...")
                pdb_dict[organism].select_camps(chainid, "ChainID")
            
            #Detect occupancy input
            if(occupancy != None):
                logging.info("Occupancy specified, aplying to object...")
                pdb_dict[organism].select_camps(occupancy, "Occupancy")
            
            #Detect order input
            if(order != None):
                logging.info("Order specified, aplying to object...")
                pdb_dict[organism].select_camps(order, "Order")

            #Detect resname input
            if(resname != '*'):
                logging.info("Residue name specified, aplying to object...")
                pdb_dict[organism].select_camps(resname, "ResName")

            #Detect serial input
            if(serial != None):
                logging.info("Serial specified, aplying to object...")
                pdb_dict[organism].select_camps(serial, "Serial")

            #Detect order range input
            if(order_min != None or order_max != None):
                logging.info("Detected range of order, minimum and maximum will be specified.")
                minimum, maximum = pdb_dict[organism].set_max_and_mins(order_min, order_max)
                logging.info("Minimum and maximum aparently specified, continuing aplying to object...")
                pdb_dict[organism].select_range(minimum, maximum, "Order")

            #Detect temp factor accurate input
            if(temp_factor_accurate != None):
                logging.info("Temperature factor accurate specified, aplying to object...")
                pdb_dict[organism].select_camps(temp_factor_accurate, "TempFactor")

            #Detect temp factor input
            if(temp_factor != None):
                logging.info("Temperature factor specified, aplying to object...")
                pdb_dict[organism].select_no_accurate(temp_factor, "TempFactor")

            #Detect temp factor range input
            if(temp_factor_range_min != None or temp_factor_range_max != None):
                logging.info("Detected range of temperature factor range, minimum and maximum will be specified.")
                minimum, maximum = pdb_dict[organism].set_max_and_mins(temp_factor_range_min, temp_factor_range_max)
                logging.info("Minimum and maximum aparently specified, continuing aplying to object...")
                pdb_dict[organism].select_range(minimum, maximum, "TempFactor")

            #Detect x accurate input
            if(x_accurate != None):
                logging.info("X accurated specified, aplying to object...")
                pdb_dict[organism].select_camps(x_accurate, "X")
            
            #Detect y accurate input
            if(y_accurate != None):
                logging.info("Y accurated specified, aplying to object...")
                pdb_dict[organism].select_camps(y_accurate, "Y")
            
            #Detect z accurate input
            if(z_accurate != None):
                logging.info("Z accurated specified, aplying to object...")
                pdb_dict[organism].select_camps(z_accurate, "Z")

            #Detect x input
            if(x_accurate != None):
                logging.info("X specified, aplying to object...")
                pdb_dict[organism].select_no_accurate(x_accurate, "X")
            
            #Detect y input
            if(y_accurate != None):
                logging.info("Y specified, aplying to object...")
                pdb_dict[organism].select_no_accurate(y_accurate, "Y")
            
            #Detect z input
            if(z_accurate != None):
                logging.info("Z specified, aplying to object...")
                pdb_dict[organism].select_no_accurate(z_accurate, "Z")

            #Detect x range input
            if(x_range_min != None or x_range_max != None):
                logging.info("Detected range X, minimum and maximum will be specified.")
                minimum, maximum = pdb_dict[organism].set_max_and_mins(x_range_min, x_range_max)
                logging.info("Minimum and maximum aparently specified, continuing aplying to object...")
                pdb_dict[organism].select_range(minimum, maximum, "X")
            
            #Detect y range input
            if(y_range_min != None or y_range_max != None):
                logging.info("Detected range Y, minimum and maximum will be specified.")
                minimum, maximum = pdb_dict[organism].set_max_and_mins(y_range_min, y_range_max)
                logging.info("Minimum and maximum aparently specified, continuing aplying to object...")
                pdb_dict[organism].select_range(minimum, maximum, "Y")
            
            #Detect z range input
            if(z_range_min != None or z_range_max != None):
                logging.info("Detected range Z, minimum and maximum will be specified.")
                minimum, maximum = pdb_dict[organism].set_max_and_mins(z_range_min, z_range_max)
                logging.info("Minimum and maximum aparently specified, continuing aplying to object...")
                pdb_dict[organism].select_range(minimum, maximum, "Z")
            """
    #Starting to apply to the return
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