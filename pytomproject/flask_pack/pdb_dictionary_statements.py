import logging

class PDB_Dictionary_Statements():
    
    pdb_dict = {}
    pdb_dict_previous = {}
    
    def __init__(self):
        pass

    #------------------------------------------------------------------------------
    # Select camps accurately from dictionary
    #------------------------------------------------------------------------------
    def select_camps(self, data, camp, organisms):
        """
        Select one or more data from one camp on one or more organism inside 
        a PDB dictionary. It will create a new dictionary with the requested 
        data.
        """
        logging.info("Selecting specified camps from atom list and applying it...")
        coincidences = 0
        new_pdb_dict = {}

        for organism in organisms:

            if(not organism in new_pdb_dict):
                new_pdb_dict[organism] = {}

            for items in self.pdb_dict[organism]["ATOM"].items():

                if(not "ATOM" in new_pdb_dict[organism]):
                    new_pdb_dict[organism]["ATOM"] = {}

                for select in data:

                    if(organism == items[1]["organism"] and items[1][camp] == select):
                        new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                        coincidences += 1

        logging.info("%i coincidences found!" % coincidences)
        logging.info("Applying changes...")
        self.pdb_dict_previous = self.pdb_dict
        self.pdb_dict = new_pdb_dict

    #------------------------------------------------------------------------------
    # Select range from dictionary
    #------------------------------------------------------------------------------
    def select_range(self, data, camp, organisms):
        """
        Select a range of data from a camp inside one or more organisms.
        It order the data automatically but only accepts two values for
        obvious reasons.
        """
        logging.info("Looking for two values...")
        failed = True

        if(len(data) == 2):
            logging.info("Found two values, are the same?")

            if(data[0] != data[1]):

                if(type(data[0] != str or type(data[1] != str))):
                    logging.info("The values %s aren't equal, sorting..." % data)
                    data = sorted(data)
                    logging.info("The values are now sorted, calling function to apply range on the PDB...")
                    datamin, datamax = (data[0], data[1])
                    logging.info("Range applyied.")
                    failed = False

                else:
                    logging.error("Can't compare a range of strings.")

            else:
                logging.error("The values are equal, try with normal or accurate mode.")

        else:
            logging.error("Wrong number of values, expected 2.")

        if(not failed):
            logging.info("Selecting specified rang from atom list and aplying it...")
            coincidences = 0
            new_pdb_dict = {}

            for organism in organisms:

                if(not organism in new_pdb_dict):
                    new_pdb_dict[organism] = {}

                for items in self.pdb_dict[organism]["ATOM"].items():

                    if(not "ATOM" in new_pdb_dict[organism]):
                        new_pdb_dict[organism]["ATOM"] = {}

                    if(organism == items[1]["organism"] and items[1][camp] < float(datamax) and items[1][camp] > float(datamin)):
                        new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                        coincidences += 1

            logging.info("%i coincidences found!" % coincidences)
            logging.info("Applying changes...")
            self.pdb_dict_previous = self.pdb_dict
            self.pdb_dict = new_pdb_dict

    #------------------------------------------------------------------------------
    # Select camps no accurate from dictionary
    #------------------------------------------------------------------------------
    def select_no_accurate(self, data, camp, organisms):
        """
        It will take the specified camps like the accurate function but
        it will don't have in consideration the decimals. For this 
        function, 43,2298 = 43,9482
        Also, this is called "Normal mode".
        """

        logging.info("Looking if the given data is a number or a string...")
        go_to_accurate = False

        for i, selection in enumerate(data):

            if(not selection.isdigit()):
                logging.warning("%s is a string! Can't apply a non accurate select." % selection)
                go_to_accurate = True
                break

            else:
                data[i] = int(data[i])

        if(go_to_accurate == False):
            logging.info("No strings in Data, non accurate select will proceed...")
            coincidences = 0
            new_pdb_dict = {}

            for organism in organisms:

                if(not organism in new_pdb_dict):
                    new_pdb_dict[organism] = {}

                for items in self.pdb_dict[organism]["ATOM"].items():

                    if(not "ATOM" in new_pdb_dict[organism]):
                        new_pdb_dict[organism]["ATOM"] = {}

                    for select in data:

                        if(organism == items[1]["organism"]):

                            if(int(items[1][camp]) == select):
                                new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                                coincidences += 1

            logging.info("%i coincidences found!" % coincidences)
            logging.info("Applying changes...")
            self.pdb_dict_previous = self.pdb_dict
            self.pdb_dict = new_pdb_dict

        else:
            logging.info("Calling select in normal mode...")
            self.select_camps(data, camp, organisms)
    
    def rollback(self):
        temp_dict = self.pdb_dict_previous
        self.pdb_dict_previous = self.pdb_dict
        self.pdb_dict = temp_dict