"""
Initialization of the databases and important function to fill them.
"""
import logging
import os
import urllib
import shutil
from . import db

"""
Flask Database Implementation tests.
"""
class Organism(db.Model):   #pylint: disable=too-few-public-methods
    """
    Class to define database relations and columns for Organism table.
    """
    name = db.Column(db.String(10), primary_key=True, unique=True)  #pylint: disable=no-member
    species = db.Column(db.String(50), default="Unassigned")    #pylint: disable=no-member
    atoms = db.relationship('Atom', backref='Atom', lazy=True)  #pylint: disable=no-member

    def __repr__(self):
        return f"Name('{self.name}', '{self.species}')"

class Atom(db.Model):   #pylint: disable=too-few-public-methods
    """
    Class to define database relations and columns for Atom table.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)   #pylint: disable=no-member
    record_type = db.Column(db.String(4), default="ATOM")   #pylint: disable=no-member
    organism = db.Column(db.String(10), db.ForeignKey('organism.name'), nullable=False) #pylint: disable=no-member
    order = db.Column(db.Integer)   #pylint: disable=no-member
    serial = db.Column(db.Integer)  #pylint: disable=no-member
    name = db.Column(db.String(4))  #pylint: disable=no-member
    altlocation = db.Column(db.String(1))   #pylint: disable=no-member
    resname = db.Column(db.String(3))   #pylint: disable=no-member
    chainid = db.Column(db.String(1))   #pylint: disable=no-member
    resseqnum = db.Column(db.Integer)   #pylint: disable=no-member
    codeinsres = db.Column(db.String(1))    #pylint: disable=no-member
    x = db.Column(db.Float) #pylint: disable=no-member
    y = db.Column(db.Float) #pylint: disable=no-member
    z = db.Column(db.Float) #pylint: disable=no-member
    occupancy = db.Column(db.Float) #pylint: disable=no-member
    tempfactor = db.Column(db.Float)    #pylint: disable=no-member
    segmentid = db.Column(db.String(4)) #pylint: disable=no-member
    elementsymbol = db.Column(db.String(2)) #pylint: disable=no-member

    def __repr__(self):
        return f"Atom('{self.organism}', '{self.record_type}', '{self.order}', \
        '{self.serial}', '{self.name}', '{self.altlocation}', '{self.resname}', \
        '{self.chainid}', '{self.resseqnum}', '{self.codeinsres}', '{self.x}', \
        '{self.y}', '{self.z}', '{self.occupancy}', '{self.tempfactor}', \
        '{self.segmentid}', '{self.elementsymbol}')"

#==============================================================================

def make_url(url_no_file="https://files.rcsb.org/download/", organism_entry="2ki5"):
    """
    Takes the download URL without the file of the PDB database and the organism entry
    and converts it in to a download link for the PDB file.

    Returns the full URL for download.
    """
    logging.info("Starting to make URL with %s and %s", url_no_file, organism_entry)
    url = url_no_file + organism_entry + ".pdb"
    logging.info("URL %s created successfuly", url)
    return url

def download_url(pdb_name, pdb_save_location, url, organism):
    """
    Receive the url, file name and save location and download the file of the url called
    "pdb_name" and saves it on "pdb_save_location".

    Return True if the download was successful and False if it wasn't and the real PDB
    file location with his name.
    """
    invalid = True
    file_exists = False
    logging.info("Starting the download procedure.")
    logging.info("Creating pdb file name.")
    pdb_name = pdb_name + organism
    pdb_save_location = pdb_save_location + "/"
    logging.info("Download file name is: %s", pdb_name + ".pdb")
    logging.info("Checking if %s exists", pdb_save_location)

    if os.path.exists(pdb_save_location):
        logging.info("%s exists, PDB will be downloaded here.", pdb_save_location)
    else:
        logging.warning("%s don't exists, trying to make it.", pdb_save_location)

        try:
            os.makedirs(pdb_save_location)
        except OSError:
            logging.critical("Can't make %s, make sure you have enough \
            permissions.", pdb_save_location)
        else:
            logging.info("Directory exist, looking for old download files.")

            if os.path.exists(pdb_save_location + pdb_name + ".pdb"):
                logging.info("Old download found, it will be used.")
                file_exists = True

    if not file_exists:

        try:
            logging.info("Trying to download from URL.")
            urllib.request.urlretrieve(url, pdb_save_location + pdb_name + ".pdb")
        except urllib.error.URLError:
            logging.critical("Download from %s failed! Make sure you writed \
            correctly the URL!", url)
        else:
            logging.info("File downloaded from %s successfuly.", url)
            invalid = False

    logging.info("Setting new data in object atributes.")

    return invalid, pdb_save_location + pdb_name + ".pdb"


def add_new_organism(name, species, url_no_file="https://files.rcsb.org/download/"):
    """
    This function will add a new organism to the database. It takes
    the organism name and specie and the download link. First it will
    create the organism on the database and download the PDB file.
    After that, it will start reading the PDB file and adding the data
    to the table Atom (which is related with the table Organism so
    every query on organism atoms will return the table atom).

    Every line starting with atom will add the information from the
    PDB and on EOF it will commit all the changes to the database.
    Once it's finished, the download folder will be deleted (if it can
    be deleted) and it will return if the creation of the database and
    the download of the file failed or not.
    """
    failed = True

    #Adding organism
    logging.info("Adding organism...")
    organism_to_add = Organism(name=name, species=species)
    logging.info("Data to add: %s, %s", name, species)
    db.session.add(organism_to_add) #pylint: disable=no-member
    db.session.commit() #pylint: disable=no-member

    #Adding atoms to organism
    url_download = make_url(url_no_file, name)
    download_results = download_url("download_", "Pytom_Downloads", url_download, name)

    if not download_results[0]:
        failed = False
        pdb_file = open(download_results[1])
        order_count = 0

        for lines in pdb_file:

            if lines.startswith("ATOM"):
                order_count += 1
                newatom = Atom(
                    record_type=lines[0:4].strip(' ') or None,
                    organism=name,
                    order=order_count,
                    serial=lines[6:10].strip(' ') or None,
                    name=lines[12:15].strip(' ') or None,
                    altlocation=lines[16].strip(' ') or None,
                    resname=lines[17:19].strip(' ') or None,
                    chainid=lines[21].strip(' ') or None,
                    resseqnum=lines[22:25].strip(' ') or None,
                    codeinsres=lines[26].strip(' ') or None,
                    x=lines[30:37].strip(' ') or None,
                    y=lines[38:45].strip(' ') or None,
                    z=lines[46:53].strip(' ') or None,
                    occupancy=lines[54:59].strip(' ') or None,
                    tempfactor=lines[60:65].strip(' ') or None,
                    segmentid=lines[72:75].strip(' ') or None,
                    elementsymbol=lines[76:78].strip(' ') or None)
                db.session.add(newatom) #pylint: disable=no-member

        db.session.commit() #pylint: disable=no-member

        logging.info("Deleting Pytom Downloads folder...")

        try:
            shutil.rmtree("Pytom_Downloads")
        except FileNotFoundError:
            logging.error("Folder not found!")
        else:
            logging.info("Folder removed successfuly!")

    else:
        logging.error("The download of the PDB file have failed! Can't continue without data.")
        logging.info("Reverting changes...")
        Organism.query.filter_by(name=name).delete()
        db.session.commit() #pylint: disable=no-member
    return failed
