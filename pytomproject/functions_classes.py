import urllib.request
import os
from operator import itemgetter
from flask import jsonify

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
                pdb_name = "downloaded_pdb.pdb", pdb_save_location = "Downloads"):
        
        """
        Initialize the variables of the object and reset some lists and dictionaries.
        """

        # Important!!! If I don't reset those "arrays" they don't delete it's content,
        # nor even in a new object!!!

        self.pdb_dictionary = None
        self.atom_list = None
        self.pdb_dictionary = {}
        self.atom_list = []
        print(self.pdb_dictionary)
        self.make_url(url_no_file, organism_entry)
        self.download_url(pdb_name, pdb_save_location)
        self.make_pdb_dictionary()
        self.make_atom_list()

    #------------------------------------------------------------------------------
    # Reset dictionary
    #------------------------------------------------------------------------------
    def reset_dictionary(self):
        self.pdb_dictionary = None
        self.pdb_dictionary = {}

    #------------------------------------------------------------------------------
    # Make atom lists
    #------------------------------------------------------------------------------
    def make_atom_list(self):
        """
        Extract all the classified PDB data from the PDB dictionary in to another
        dictionary but without classify for manipulate the output.
        """
        for entries1 in self.pdb_dictionary.items():
            for entries2 in entries1[1].items():
                self.atom_list.append(entries2[1])

    #------------------------------------------------------------------------------
    # Make atom lists setting the atom
    #------------------------------------------------------------------------------
    def make_atom_list_atom(self, atom_name):
        """
        Extract all the classified PDB data from the PDB dictionary in to another
        dictionary but without classify for manipulate the output.
        It does the same thing as the function above, except it takes the atom name
        specified.
        """
        result = []
        for atoms in self.atom_list:
            if(atoms["Name"] == atom_name):
                result.append(atoms)
        self.atom_list = None
        self.atom_list = result
        
    #------------------------------------------------------------------------------
    # Make PDB_Dictionary
    #------------------------------------------------------------------------------
    def make_pdb_dictionary(self):
        """
        Export every atom of the downloaded PDB into dictionaries, classifing them
        by its atom names.
        """
        pdb_file = open(self.path + self.name, "r")
        index_atom = {}
        index_all = 0
        for lines in pdb_file:
            if(lines.startswith("ATOM")):
                atom_name = lines[12:16].strip(' ')
                index_all += 1
                if(atom_name not in self.pdb_dictionary):
                    index_atom[atom_name] = 0
                    self.pdb_dictionary[atom_name] = {index_atom[atom_name]:
                    {"Organism": self.organism,
                    "Order": index_all,
                    "Data": lines[0:5].strip(' ') or None,
                    "Serial": int(lines[6:10].strip(' ') or 0),
                    "Name": lines[12:16].strip(' ') or None,
                    "AltLocation": lines[16].strip(' ') or None,
                    "ResName": lines[17:19].strip(' ') or None,
                    "ChainID": lines[21].strip(' ') or None,
                    "ResSeqNum": int(lines[22:25].strip(' ') or 0),
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
                    index_atom[atom_name] += 1
                    self.pdb_dictionary[atom_name].update({index_atom[atom_name]:
                    {"Organism": self.organism,
                    "Order": index_all,
                    "Data": lines[0:5].strip(' ') or None,
                    "Serial": int(lines[6:10].strip(' ') or 0),
                    "Name": lines[12:16].strip(' ') or None,
                    "AltLocation": lines[16].strip(' ') or None,
                    "ResName": lines[17:19].strip(' ') or None,
                    "ChainID": lines[21].strip(' ') or None,
                    "ResSeqNum": int(lines[22:25].strip(' ') or 0),
                    "CodInsRes": lines[26].strip(' ') or None,
                    "X": float(lines[30:37].strip(' ') or 0),
                    "Y": float(lines[38:45].strip(' ') or 0),
                    "Z": float(lines[46:53].strip(' ') or 0),
                    "Occupancy": float(lines[54:59].strip(' ') or 0),
                    "TempFactor": float(lines[60:65].strip(' ') or 0),
                    "SegmentID": lines[72:75].strip(' ') or None,
                    "ElementSymbol": lines[76:78].strip(' ').strip('\n') or None
                    }})

    #------------------------------------------------------------------------------
    # Make URL
    #------------------------------------------------------------------------------
    def make_url(self, url_no_file = "https://files.rcsb.org/download/", organism_entry = "2ki5"):
        """
        Takes the download URL without the file of the PDB database and the organism entry 
        and converts it in to a download link for the PDB file.

        Returns the full URL for download.
        """
        print("Making URL...")
        url = url_no_file + organism_entry + ".pdb"
        self.organism = organism_entry
        print("Url %s created." % url)

        self.url = url

    #------------------------------------------------------------------------------  
    # Download URL
    #------------------------------------------------------------------------------
    def download_url(self, pdb_name = "downloaded_pdb.pdb", pdb_save_location = "Downloads"):
        """
        Receive the url, file name and save location and download the file of the url called
        "pdb_name" and saves it on "pdb_save_location".

        Return True if the download was successful and False if it wasn't.
        """

        print("Checking if directory exists...")
        if(os.path.exists(pdb_save_location)):
            print("Directory %s exist." % pdb_save_location)
        else:
            print("Directory %s don't exists, creating it..." % pdb_save_location)
            try:
                os.makedirs(pdb_save_location)
            except OSError:
                print("Creation of the directory %s failed" % pdb_save_location)
            else:
                print("Successfully created the directory %s" % pdb_save_location)
                print("Checking if file exists...")
                if(os.path.exists(pdb_save_location + ".pdb")):
                    os.remove(pdb_save_location + ".pdb")
        print("Beginning file download...")
        try:
            urllib.request.urlretrieve(self.url, pdb_save_location + pdb_name)
        except ValueError:
            print("Download of %s failed." % self.url)
        else:
            print("File downloaded correctly on %s" % pdb_save_location)

        self.path = pdb_save_location
        self.name = pdb_name  

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
        print(question)
        answer = input("Yes (y) or no (n): ")
        answer = str(answer[0]).lower()
    return answer

