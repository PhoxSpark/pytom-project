import urllib, os, logging, sys
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
    
    logging.info("****************************************************************************************************")
    logging.info("Test Information message: This messages will inform about what the program is doing.")
    logging.warning("Test warning message: This messages will advise you about something.")
    logging.error("Test error message: This messages will inform about problems while executing the program.")
    logging.critical("Test critical message: This messages will inform about major problems in the program that may can interrumpt it.")
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