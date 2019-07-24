"""
All dictionary operations, classes and functions.
"""
import logging
from flask import jsonify

def go_to_accurate_function(go_to_accurate, data):
    """
    Determine if normal mode has to go to accurate mode.
    """
    for i, selection in enumerate(data):
        if not isinstance(selection, int) and not isinstance(selection, float):
            if not selection.isdigit():
                logging.warning("%s is a string! Can't apply a non accurate select.", selection)
                go_to_accurate = True
                break
            else:
                logging.info("Converting %s in to integer.", data[i])
                data[i] = int(data[i])
    return go_to_accurate, data

class PdbDictionaryStatements():
    """
    Dictionary data and functions.
    """
    failed = False
    pdb_dict = {}
    pdb_dict_previous = {}
    json = None
    organism_list = []

    def __init__(self):
        logging.info("PDB_Dictionary initialized.")

    def select_camps(self, data, camp):
        """
        Select one or more data from one camp on one or more organism inside
        a PDB dictionary. It will create a new dictionary with the requested
        data.
        """
        logging.info("Selecting specified camps from atom list and applying it...")
        coincidences = 0
        new_pdb_dict = {}
        logging.info("Organisms to look: %s", self.organism_list)
        for organism in self.organism_list:
            logging.debug("Looking for value/s %s on camp %s inside organism %s...", \
            data, camp, organism)

            if not organism in new_pdb_dict:
                new_pdb_dict[organism] = {}

            for items in self.pdb_dict[organism]["ATOM"].items():

                if not "ATOM" in new_pdb_dict[organism]:
                    new_pdb_dict[organism]["ATOM"] = {}

                for select in data:

                    if(organism == items[1]["organism"] and items[1][camp] == select):
                        new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                        coincidences += 1

        if coincidences > 0:
            logging.info("%i coincidences found!", coincidences)
            logging.info("Applying changes...")
            self.pdb_dict_previous = self.pdb_dict
            self.pdb_dict = new_pdb_dict
        else:
            logging.info("No coincidences, changes will not be applyied.")


    def set_range(self, data):
        """
        Set range to look in to the dictionary.
        """
        if len(data) == 2:
            logging.info("Found two values, are the same?")

            if data[0] != data[1]:

                if type(data[0] != str or type(data[1] != str)):
                    logging.info("The values %s aren't equal, sorting...", data)
                    data = sorted(data)
                    logging.info("The values are now sorted, calling function to \
                    apply range on the PDB...")
                    datamin, datamax = (data[0], data[1])
                    logging.info("Range applyied.")
                    self.failed = False

                else:
                    logging.error("Can't compare a range of strings.")

            else:
                logging.error("The values are equal, try with normal or accurate mode.")

        else:
            logging.error("Wrong number of values, expected 2.")

        return datamin, datamax

    def select_range(self, data, camp):
        """
        Select a range of data from a camp inside one or more self.organism_list.
        It order the data automatically but only accepts two values for
        obvious reasons.
        """
        logging.info("Looking for two values...")
        self.failed = True

        datamin, datamax = self.set_range(data)

        if not self.failed:
            logging.info("Selecting specified range from atom list and aplying it...")
            coincidences = 0
            new_pdb_dict = {}
            logging.info("Organisms to look: %s", self.organism_list)
            for organism in self.organism_list:
                logging.debug("Looking for value/s %s on camp %s inside organism %s...", \
                data, camp, organism)

                if not organism in new_pdb_dict:
                    new_pdb_dict[organism] = {}

                for items in self.pdb_dict[organism]["ATOM"].items():

                    if not "ATOM" in new_pdb_dict[organism]:
                        new_pdb_dict[organism]["ATOM"] = {}

                    if organism == items[1]["organism"] and \
                    items[1][camp] <= float(datamax) and \
                    items[1][camp] >= float(datamin):
                        new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                        coincidences += 1
                        logging.debug("Coincidence found!")
                    else:
                        logging.debug("%s is not between %s and %s.", \
                        items[1]["organism"] and items[1][camp], float(datamin), float(datamax))

            if coincidences > 0:
                logging.info("%i coincidences found!", coincidences)
                logging.info("Applying changes...")
                self.pdb_dict_previous = self.pdb_dict
                self.pdb_dict = new_pdb_dict
            else:
                logging.info("No coincidences, changes will not be applyied.")

    def select_no_accurate(self, data, camp):
        """
        It will take the specified camps like the accurate function but
        it will don't have in consideration the decimals. For this
        function, 43,2298 = 43,9482
        Also, this is called "Normal mode".
        """
        go_to_accurate = False
        logging.info("Looking if the given data is a number or a string...")
        go_to_accurate, data = go_to_accurate_function(go_to_accurate, data)
        if not go_to_accurate:
            logging.info("No strings in Data, non accurate select will proceed...")
            coincidences = 0
            new_pdb_dict = {}
            logging.info("Organisms to look: %s", self.organism_list)
            for organism in self.organism_list:

                if not organism in new_pdb_dict:
                    new_pdb_dict[organism] = {}

                for items in self.pdb_dict[organism]["ATOM"].items():

                    if not "ATOM" in new_pdb_dict[organism]:
                        new_pdb_dict[organism]["ATOM"] = {}

                    for select in data:

                        if organism == items[1]["organism"] and int(items[1][camp]) == select:
                            new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                            coincidences += 1

            if coincidences > 0:
                logging.info("%i coincidences found!", coincidences)
                logging.info("Applying changes...")
                self.pdb_dict_previous = self.pdb_dict
                self.pdb_dict = new_pdb_dict
            else:
                logging.info("No coincidences, changes will not be applyied.")
        else:
            logging.info("Calling select in normal mode...")
            self.select_camps(data, camp)

    def rollback(self, test=False):
        """
        Simple but useful function to come back to last dictionary.
        """
        temp_dict = self.pdb_dict_previous
        self.pdb_dict_previous = self.pdb_dict
        self.pdb_dict = temp_dict
        if not test:
            self.jsonify()

    def jsonify(self):
        """
        Transforms a dictionary in to a json file. The class atribute is
        called json because it's expected to contain jsonified dictionaries
        but it can contain templates and renders from flask.
        """
        logging.info("Clearing json variable...")
        self.json = None
        logging.info("Applying changes to the json variable...")
        self.json = jsonify(self.pdb_dict)

    def organism_list_add(self, organism):
        """
        Add organisms to the Class variable if it doesn't exists yet.
        """
        for items in organism:
            if items not in self.organism_list:
                self.organism_list.append(items)
