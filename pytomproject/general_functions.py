#
"""
General poutpose functions
"""
import os
import logging
import pickle

#------------------------------------------------------------------------------
# Split word
#------------------------------------------------------------------------------
def split(word):
    """
    Simple function to convert every string send it to him in to
    a list of single characters.
    """
    list_word = []

    for character in word:
        list_word.append(character)

    return list_word

#------------------------------------------------------------------------------
# Save object to Pickle
#------------------------------------------------------------------------------
def save_obj(obj, name):
    """
    This function transforms every object send it to him in to a .pkl
    file for future load an persistency of the data.
    """
    if not os.path.exists("data/"):
        logging.info("Path don't exists, creating it.")
        os.makedirs("data/")

    with open("data/"+ name + ".pkl", "wb") as file:
        logging.info("Saving...")
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)
        logging.info("File saved.")

#------------------------------------------------------------------------------
# Load object from Pickle
#------------------------------------------------------------------------------
def load_obj(name):
    """
    This function can load the .pkl files saved in to an object of the
    same type.
    """
    object_load = {}

    logging.info("Looking if the file exists...")
    if os.path.exists("data/" + name + ".pkl"):
        logging.info("File exists, it will be loaded.")
        with open("data/" + name + ".pkl", "rb") as file:
            object_load = pickle.load(file)

    return object_load
