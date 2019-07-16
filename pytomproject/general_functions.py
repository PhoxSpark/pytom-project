import urllib, os, logging, sys, pickle
from datetime import datetime

#==============================================================================
# General pourpose functions
#==============================================================================

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
    logging.info("Starting simple question procedure...")
    answer = ''

    while(answer != 'n' and answer != 'y'):
        answer = input("Yes (y) or no (n): ")
        answer = str(answer[0]).lower()

    logging.info("Procedure finished, returning answer...")

    return answer

#------------------------------------------------------------------------------
# Save object to Pickle
#------------------------------------------------------------------------------
def save_obj(obj, name):
    """
    This function transforms every object send it to him in to a .pkl
    file for future load an persistency of the data.
    """
    if(not os.path.exists("data/")):
        os.makedirs("data/")

    with open("data/"+ name + ".pkl", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

#------------------------------------------------------------------------------
# Load object from Pickle
#------------------------------------------------------------------------------
def load_obj(name):
    """
    This function can load the .pkl files saved in to an object of the
    same type.
    """
    object_load = {}

    if(os.path.exists("data/" + name + ".pkl")):

        with open("data/" + name + ".pkl", "rb") as f:
            object_load = pickle.load(f)
            
    return object_load
