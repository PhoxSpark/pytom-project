import urllib.request
import os, logging
from operator import itemgetter
from flask import jsonify

#-----------------Log block-------------------
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO)
#---------------------------------------------

#==============================================================================
# Classes
#==============================================================================

#------------------------------------------------------------------------------
# PDB
#------------------------------------------------------------------------------

class Object_PDB():
    """
    This object initialize downloading the PDB file and saving important data about it
    like the URL (not so important after download), the path where it was downloaded and
    the name of the file. Also takes the PDB and save it's data on a dictionary for 
    future use.
    """

    organism = ""
    url = ""
    path = ""
    name = ""
    pdb_dictionary = {}
    atom_list = []


    #------------------------------------------------------------------------------
    # Class Initialization
    #------------------------------------------------------------------------------
    def __init__(self, organism_entry = "2ki5", url_no_file = "https://files.rcsb.org/download/", 
                pdb_name = "download_", pdb_save_location = "Pytom_Downloads"):
        
        """
        Initialize the variables of the object and reset some lists and dictionaries.
        """

        # Important!!! If I don't reset those "arrays" they don't delete it's content,
        # nor even in a new object!!!

        logging.info("Class initializing")
        logging.info("Setting empty atributes")
        self.pdb_dictionary = None
        self.atom_list = None
        self.pdb_dictionary = {}
        logging.info("PDB_DICTIONARY restarted")
        self.atom_list = []
        logging.info("ATOM_LIST restarted")

        logging.info("Filling important data and downloading PDB")
        logging.info("Creating URL")
        self.make_url(url_no_file, organism_entry)
        logging.info("Downloading to path using URL")
        self.download_url(pdb_name, pdb_save_location)
        logging.info("Extracting data from PDB to dictionary")
        self.make_pdb_dictionary()
        logging.info("Making list of atoms with less data")
        self.make_atom_list()
        logging.info("Initialization successful")

    #------------------------------------------------------------------------------
    # Make atom list
    #------------------------------------------------------------------------------
    def make_atom_list(self):
        """
        Extract all the classified PDB data from the PDB dictionary in to another
        dictionary but without classify for manipulate the output.
        """
        logging.info("Making Atom list")
        for entries1 in self.pdb_dictionary.items():
            logging.debug("Accessing to dictionary items row")
            for entries2 in entries1[1].items():
                logging.debug("Adding atom to atom_list")
                self.atom_list.append(entries2[1])
        logging.info("Atom list created successfully")

    #------------------------------------------------------------------------------
    # Select camps
    #------------------------------------------------------------------------------
    def select_camps(self, data, camp):
        
        logging.info("Selecting specified camps from atom list and aplying it")
        result = []
        for atoms in self.atom_list:
            if(atoms[camp] == data):
                logging.debug("Coincidence found")
                result.append(atoms)
        self.atom_list = None
        self.atom_list = result
        logging.info("Changes applied on atom list")
        
    #------------------------------------------------------------------------------
    # Select range
    #------------------------------------------------------------------------------
    def select_range(self, datamin, datamax, camp):
        
        logging.info("Selecting specified rang from atom list and aplying it")
        result = []
        for atoms in self.atom_list:
            if(atoms[camp] < datamax and atoms[camp] > datamin):
                logging.debug("Coincidence found")
                result.append(atoms)
        self.atom_list = None
        self.atom_list = result
        logging.info("Changes applied on atom list")

        
    #------------------------------------------------------------------------------
    # Set function friendly ranges
    #------------------------------------------------------------------------------
    def set_max_and_mins(self, datamin = None, datamax = None):

        logging.info("Creating a rang with max or minimum specified. If it's not specified it will take almost infinite value (negative for min, positive for max)")
        minimum = -999999999
        maximum = 999999999
        if(datamin != None):
            logging.info("Minimum specified, setting it to %f" % datamin)
            minimum = datamin
        if(datamax != None):
            logging.info("Maximum specified, setting it to %f" % datamax)
            maximum = datamax
        
        return minimum, maximum


    #------------------------------------------------------------------------------
    # Make PDB_Dictionary
    #------------------------------------------------------------------------------
    def make_pdb_dictionary(self):
        """
        Export every atom of the downloaded PDB into dictionaries, classifing them
        by its atom names.
        """
        logging.info("Starting to make PDB dictionary from PDB file")
        logging.info("Opening PDB file in read mode")
        pdb_file = open(self.path + self.name, "r")
        logging.info("Starting index")
        index_atom = {}
        index_all = 0
        logging.info("Reading PDB lines")
        for lines in pdb_file:
            logging.debug("Testing if the line starts with ATOM")
            if(lines.startswith("ATOM")):
                logging.debug("Selecting atom name for classification")
                atom_name = lines[12:16].strip(' ')
                index_all += 1
                logging.debug("Testing if %s exists in dictionary" % atom_name)
                if(atom_name not in self.pdb_dictionary):
                    logging.debug("%s don't exists, creating it and filling it with data" % atom_name)
                    index_atom[atom_name] = 0
                    self.pdb_dictionary[atom_name] = {index_atom[atom_name]:
                    {"Organism": self.organism,
                    "Order": index_all,
                    "Data": lines[0:5].strip(' ') or None,
                    "Serial": float(lines[6:10].strip(' ') or 0),
                    "Name": lines[12:16].strip(' ') or None,
                    "AltLocation": lines[16].strip(' ') or None,
                    "ResName": lines[17:19].strip(' ') or None,
                    "ChainID": lines[21].strip(' ') or None,
                    "ResSeqNum": float(lines[22:25].strip(' ') or 0),
                    "CodInsRes": lines[26].strip(' ') or None,
                    "X": float(lines[30:37].strip(' ') or 0),
                    "Y": float(lines[38:45].strip(' ') or 0),
                    "Z": float(lines[46:53].strip(' ') or 0),
                    "Occupancy": float(lines[54:59].strip(' ') or 0),
                    "TempFactor": float(lines[60:65].strip(' ') or 0),
                    "SegmentID": lines[72:75].strip(' ') or None,
                    "ElementSymbol": lines[76:78].strip(' ').strip('\n') or None
                    }}
                else:
                    logging.debug("%s exists, adding data" % atom_name)
                    index_atom[atom_name] += 1
                    self.pdb_dictionary[atom_name].update({index_atom[atom_name]:
                    {"Organism": self.organism,
                    "Order": index_all,
                    "Data": lines[0:5].strip(' ') or None,
                    "Serial": float(lines[6:10].strip(' ') or 0),
                    "Name": lines[12:16].strip(' ') or None,
                    "AltLocation": lines[16].strip(' ') or None,
                    "ResName": lines[17:19].strip(' ') or None,
                    "ChainID": lines[21].strip(' ') or None,
                    "ResSeqNum": float(lines[22:25].strip(' ') or 0),
                    "CodInsRes": lines[26].strip(' ') or None,
                    "X": float(lines[30:37].strip(' ') or 0),
                    "Y": float(lines[38:45].strip(' ') or 0),
                    "Z": float(lines[46:53].strip(' ') or 0),
                    "Occupancy": float(lines[54:59].strip(' ') or 0),
                    "TempFactor": float(lines[60:65].strip(' ') or 0),
                    "SegmentID": lines[72:75].strip(' ') or None,
                    "ElementSymbol": lines[76:78].strip(' ').strip('\n') or None
                    }})
        logging.info("Dictionary created successfuly")

    #------------------------------------------------------------------------------
    # Make URL
    #------------------------------------------------------------------------------
    def make_url(self, url_no_file = "https://files.rcsb.org/download/", organism_entry = "2ki5"):
        """
        Takes the download URL without the file of the PDB database and the organism entry 
        and converts it in to a download link for the PDB file.

        Returns the full URL for download.
        """
        logging.info("Starting to make URL with %s and %s" % (url_no_file, organism_entry))
        url = url_no_file + organism_entry + ".pdb"
        logging.info("URL %s created successfuly" % url)
        logging.info("Aplying to atributes")
        self.organism = organism_entry
        self.url = url

    #------------------------------------------------------------------------------  
    # Download URL
    #------------------------------------------------------------------------------
    def download_url(self, pdb_name = "download_", pdb_save_location = "Downloads"):
        """
        Receive the url, file name and save location and download the file of the url called
        "pdb_name" and saves it on "pdb_save_location".

        Return True if the download was successful and False if it wasn't.
        """
        file_exists = False
        logging.info("Starting the download procedure")
        logging.info("Creating pdb file name")
        pdb_name = pdb_name + self.organism
        pdb_save_location = pdb_save_location + "/"
        logging.info("Download file name is: %s" % pdb_name + ".pdb")
        logging.info("Checking if %s exists" % pdb_save_location)
        if(os.path.exists(pdb_save_location)):
            logging.info("%s exists, PDB will be downloaded here" % pdb_save_location)
        else:
            logging.warning("%s don't exists, trying to make it" % pdb_save_location)
            try:
                os.makedirs(pdb_save_location)
            except OSError:
                logging.critical("Can't make %s, make sure you have enough permissions" % pdb_save_location)
            else:
                logging.info("Directory exist, looking for old download files")
                if(os.path.exists(pdb_save_location + pdb_name + ".pdb")):
                    logging.info("Old download found, it will be used")
                    file_exists = True
        if(not file_exists):
            try:
                logging.info("Trying to download from URL")
                urllib.request.urlretrieve(self.url, pdb_save_location + pdb_name + ".pdb")
            except ValueError:
                logging.error("Download from %s failed! Make sure you writed correctly the URL!" % self.url)
            else:
                logging.info("File downloaded from %s successfuly" % self.url)

        logging.info("Setting new data in object atributes")
        self.path = pdb_save_location
        self.name = pdb_name + ".pdb"

#==============================================================================
# Functions
#==============================================================================

#------------------------------------------------------------------------------
# Question Y/N
#------------------------------------------------------------------------------
def question_y_n(question=""):
    """
    Send them an answer and it will return a 'y' or 'n'. It will not 
    continue with answers differents than Yes or No. It only takes 
    the user answer first character and make it lower for return and 
    testing.

    Returns 'y' or 'n'
    """
    answer = ''
    while(answer != 'n' and answer != 'y'):
        answer = input("Yes (y) or no (n): ")
        answer = str(answer[0]).lower()
    return answer

