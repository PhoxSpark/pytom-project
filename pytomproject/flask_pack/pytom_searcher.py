import urllib, os, logging

#==============================================================================
# Pytom Searcher
#==============================================================================

#------------------------------------------------------------------------------
# Class PDB
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
    invalid = True


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

        logging.info("Class initializing...")
    
        logging.info("Setting empty atributes...")
        self.pdb_dictionary = None
        logging.debug("PDB_DICTIONARY = None")
        self.atom_list = None
        logging.debug("ATOM_LIST = None")
        self.pdb_dictionary = {}
        logging.debug("PDB_DICTIONARY restarted")
        self.atom_list = []
        logging.debug("ATOM_LIST restarted")

        logging.info("Atributes are empty, filling them with important data from the PDB specified (%s)..." % organism_entry)

        logging.info("Creating URL...")
        self.make_url(url_no_file, organism_entry)
        logging.info("URL %s created, Downloading PDB from it..." % self.url)
        self.download_url(pdb_name, pdb_save_location)
        if(self.invalid == False):
            logging.info("File downloaded, extracting data to a dictionary...")
            self.invalid = False
            self.make_pdb_dictionary()
            logging.info("Data extracted successfuly, making list...")
            self.make_atom_list()
            logging.info("List created successfuly. Initialization completed.")
        else:
            logging.error("Object can't be maded with a failed download!")
        

    #------------------------------------------------------------------------------
    # Make atom list
    #------------------------------------------------------------------------------
    def make_atom_list(self):
        """
        Extract all the classified PDB data from the PDB dictionary in to another
        dictionary but without classify for manipulate the output.
        """
        logging.info("Making Atom list...")

        for entries1 in self.pdb_dictionary.items():
            for entries2 in entries1[1].items():
                self.atom_list.append(entries2[1])

        logging.info("Atom list created successfully.")

    #------------------------------------------------------------------------------
    # Select camps
    #------------------------------------------------------------------------------
    def select_camps(self, data, camp):
        
        logging.info("Selecting specified camps from atom list and applying it...")
        coincidences = 0
        result = []
        for selection in data:
            logging.info("Looking for %s" % selection)
            for atoms in self.atom_list:
                if(atoms[camp] == selection):
                    result.append(atoms)
                    coincidences += 1

        logging.info("%i coincidences found!" % coincidences)
        logging.info("Applying changes...")
        self.atom_list = None
        self.atom_list = result

        logging.info("Changes applied on atom list.")
        
    #------------------------------------------------------------------------------
    # Select range
    #------------------------------------------------------------------------------
    def select_range(self, datamin, datamax, camp):
        

        logging.info("Selecting specified rang from atom list and aplying it...")
        coincidences = 0
        result = []
        for atoms in self.atom_list:
            if(atoms[camp] < float(datamax) and atoms[camp] > float(datamin)):
                result.append(atoms)
                coincidences += 1

        logging.info("%i coincidences found!" % coincidences)
        logging.info("Applying changes...")
        self.atom_list = None
        self.atom_list = result
        
        logging.info("Changes applied on atom list.")

    #------------------------------------------------------------------------------
    # Select unnaccurate values
    #------------------------------------------------------------------------------
    def select_no_accurate(self, data, camp):

        logging.info("Looking if the given data is a number or a string...")
        go_to_accurate = False
        for selection in data:
            if(type(selection) == str):
                logging.warning("Detected string! Can't apply a non accurate select.")
                go_to_accurate = True
                break
        if(go_to_accurate == False):
            logging.info("No strings in Data, non accurate select will proceed...")
            coincidences = 0
            result = []
            for selection in data:
                logging.info("Looking for %s" % selection)
                for atoms in self.atom_list:
                    if(int(atoms[camp]) == selection):
                        result.append(atoms)
                        coincidences += 1

            logging.info("%i coincidences found!" % coincidences)
            logging.info("Applying changes...")
            self.atom_list = None
            self.atom_list = result

            logging.info("Changes applied on atom list.")
        else:
            logging.info("Calling select in normal mode...")
            self.select_camps(data, camp)
        
    #------------------------------------------------------------------------------
    # Set function friendly ranges
    #------------------------------------------------------------------------------
    def set_max_and_mins(self, datamin = None, datamax = None):
        """
        This function takes a minimum and maximum and determine if their are valid.
        If there is no max or min, they will be assigned to an exagerated number with
        the objective of get an "until last" range.

        It returns minimum and maximum value.
        """
        logging.info("Creating a rang with max or minimum specified. If it's not specified it will take almost infinite value (negative for min, positive for max)")
        minimum = -999999999
        maximum = 999999999
        if(datamin != None):
            logging.info("Minimum specified, setting it to %f" % datamin)
            minimum = datamin
        if(datamax != None):
            logging.info("Maximum specified, setting it to %f" % datamax)
            maximum = datamax
        logging.info("Range created successfuly, returning it.")
        return minimum, maximum


    #------------------------------------------------------------------------------
    # Make PDB_Dictionary
    #------------------------------------------------------------------------------
    def make_pdb_dictionary(self):
        """
        Export every atom of the downloaded PDB into dictionaries, classifing them
        by its atom names.
        """
        logging.info("Starting to make PDB dictionary from PDB file.")
        logging.info("Opening PDB file in read mode.")
        pdb_file = open(self.path + self.name, "r")
        logging.info("PDB file aparently opened.")

        logging.info("Starting index...")
        index_atom = {}
        index_all = 0
        logging.info("Trying to read PDB lines...")
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
        logging.info("Dictionary created successfuly. %i Atoms found." % index_all)

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
        logging.info("Starting the download procedure.")
        logging.info("Creating pdb file name.")
        pdb_name = pdb_name + self.organism
        pdb_save_location = pdb_save_location + "/"
        logging.info("Download file name is: %s" % pdb_name + ".pdb")
        logging.info("Checking if %s exists" % pdb_save_location)
        if(os.path.exists(pdb_save_location)):
            logging.info("%s exists, PDB will be downloaded here." % pdb_save_location)
        else:
            logging.warning("%s don't exists, trying to make it." % pdb_save_location)
            try:
                os.makedirs(pdb_save_location)
            except OSError:
                logging.critical("Can't make %s, make sure you have enough permissions." % pdb_save_location)
            else:
                logging.info("Directory exist, looking for old download files.")
                if(os.path.exists(pdb_save_location + pdb_name + ".pdb")):
                    logging.info("Old download found, it will be used.")
                    file_exists = True
        if(not file_exists):
            try:
                logging.info("Trying to download from URL.")
                urllib.request.urlretrieve(self.url, pdb_save_location + pdb_name + ".pdb")
            except urllib.error.URLError:
                logging.critical("Download from %s failed! Make sure you writed correctly the URL!" % self.url)
            else:
                logging.info("File downloaded from %s successfuly." % self.url)
                self.invalid = False

        logging.info("Setting new data in object atributes.")
        self.path = pdb_save_location
        self.name = pdb_name + ".pdb"

    #------------------------------------------------------------------------------
    # Select statement
    #------------------------------------------------------------------------------
    def select_function(self, select, organism):
                    
        """
        Select statement for use with PDB
        
        This custom select can take a range of values, a list of accurate values
        or a list of general values (ignoring decimals). The sintax it's unique
        (unfortunately), but it can be used in the URL of flask and it has pretty
        simple options.

        Sintax: This statement comes before the organism, it starts with 
        "&select=" (without quotes). The default order for the values are:
        1. Value: Value inside of the camp of a PDB that we want to select. 
                It's a list so it accepts multiple values separated by ",".
                
        2. Camp: The camp is the container of values that we are looking for,
                for example: Name. It's case sensitive.

        3. Mode: There are 3 different modes:

            Normal: It will take the values (integer/float) and select the same 
            without considering decimals.

            Range: Takes two values and show all the data between them.

            Accurate: Takes a list of floats and return the exact coincidences.

        Example of use standard:    ?organism=2ki5&select=40,41;X;normal
        Example of alternative use: ?organism=2ki5&select=mode:range;value:40,42;camp:X

        This two examples do almost the same.
        """

        # This part will order the input in to a list
        logging.info("Spliting the string...")
        select = select.split(';')
        select_list = [None, None, None]
        logging.info("Checking data and ordering them...")
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
        
        logging.info("Arguments added to the list: %s, this have 3 data requirements so every other data will be ignored. Proceeding to call the function to apply to PDB object." % select_list)
        
        #This will determine the mode and act in consequence calling the existing functions to do the work.
        if(select_list[2] == "normal"):
            logging.info("Normal mode recogniced, proceeding...")
            self.select_no_accurate(select_list[0], select_list[1])

        elif(select_list[2] == "range"):
            logging.info("Range mode recogniced, looking for two values...")

            if(len(select_list[0]) == 2):
                logging.info("Found two values, are the same?")

                if(select_list[0][0] != select_list[0][1]):
                    logging.info("The values %s aren't equal, sorting..." % select_list[0])
                    select_list[0] = sorted(select_list[0])
                    logging.info("The values are now sorted, calling function to apply range on the PDB...")
                    self.select_range(select_list[0][0], select_list[0][1], select_list[1])
                    logging.info("Range applyied.")

                else:
                    logging.error("The values are equal, try with normal mode.")

            else:
                logging.error("Wrong number of values, expected 2.")
                

        elif(select_list[2] == "accurate"):
            logging.info("Accurate mode recogniced, proceeding...")
            self.select_camps(select_list[0], select_list[1])
            
        else:
            logging.error("The specified mode (%s) is not recogniced, select will not proceed." % select_list[2])