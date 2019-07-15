import urllib, os, logging, sys, pickle
from datetime import datetime

#==============================================================================
# General pourpose functions
#==============================================================================

#------------------------------------------------------------------------------
# Initialize Logger
#------------------------------------------------------------------------------

def initialize_logger(argument):
    """
    Selfexplanatory, but it initializes the logging system.
    """

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Start console logging system.

    if("file-logging" in argument):
        if(not os.path.exists("log/")):
            os.makedirs("log/")
        now = datetime.now()
        logging.basicConfig(filename='log/pytom-log-%s.log' % now.strftime("%d_%m_%Y-%H:%M:%S"), level=logging.DEBUG, format="%(asctime)s-[%(levelname)s]: %(message)s")

    if("console-logging" in argument):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s-[%(levelname)s]: %(message)s")
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        root.addHandler(handler)
    
    if("file-logging" in argument or "console-logging" in argument):
        logging.info("****************************************************************************************************")
        logging.info("Test Information message: This messages will inform about what the program is doing.")
        logging.warning("Test warning message: This messages will advise you about something.")
        logging.error("Test error message: This messages will inform about problems while executing the program.")
        logging.critical("Test critical message: This messages will inform about major problems in the program that may interrumpt it.")
        logging.debug("Test debug message: This messages are for the programmers, it will display some useful information.")
        logging.info("****************************************************************************************************")

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

def save_obj(obj, name ):
    if(not os.path.exists("data/" + name + ".pkl")):
        os.makedirs("data/")
    with open("data/"+ name + ".pkl", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    object_load = {}
    if(os.path.exists("data/" + name + ".pkl")):
        with open("data/" + name + ".pkl", "rb") as f:
            object_load = pickle.load(f)
    return object_load

def select_camps(data, camp, pdb_dict, organisms):
    """
    """
    logging.info("Selecting specified camps from atom list and applying it...")
    coincidences = 0
    new_pdb_dict = {}

    for organism in organisms:
        if(not organism in new_pdb_dict):
            new_pdb_dict[organism] = {}
        for items in pdb_dict[organism]["ATOM"].items():
            if(not "ATOM" in new_pdb_dict[organism]):
                new_pdb_dict[organism]["ATOM"] = {}
            for select in data:
                if(organism == items[1]["organism"] and items[1][camp] == select):
                    new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                    coincidences += 1
    logging.info("%i coincidences found!" % coincidences)
    logging.info("Applying changes...")
    return new_pdb_dict

def select_range(datamin, datamax, camp, pdb_dict, organisms):
    """
    """
    logging.info("Selecting specified rang from atom list and aplying it...")

    coincidences = 0
    new_pdb_dict = {}
    for organism in organisms:
        if(not organism in new_pdb_dict):
            new_pdb_dict[organism] = {}
        for items in pdb_dict[organism]["ATOM"].items():
            if(not "ATOM" in new_pdb_dict[organism]):
                new_pdb_dict[organism]["ATOM"] = {}
            if(organism == items[1]["organism"] and items[1][camp] < float(datamax) and items[1][camp] > float(datamin)):
                new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                coincidences += 1

    logging.info("%i coincidences found!" % coincidences)
    logging.info("Applying changes...")
    return new_pdb_dict
    
def select_no_accurate(data, camp, pdb_dict, organisms):
    """
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
            for items in pdb_dict[organism]["ATOM"].items():
                if(not "ATOM" in new_pdb_dict[organism]):
                    new_pdb_dict[organism]["ATOM"] = {}
                for select in data:
                    if(organism == items[1]["organism"]):
                        if(int(items[1][camp]) == select):
                            new_pdb_dict[organism]["ATOM"][items[0]] = items[1]
                            coincidences += 1        
        logging.info("%i coincidences found!" % coincidences)
        logging.info("Applying changes...")
        return new_pdb_dict

    else:
        logging.info("Calling select in normal mode...")
        return select_camps(data, camp, pdb_dict, organisms)
    
    