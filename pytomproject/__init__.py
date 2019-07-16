import os, logging, sys
from .flask_pack.general_functions import split
from datetime import datetime

#------------------------------------------------------------------------------
# Take arguments
#------------------------------------------------------------------------------
argument = []
flags = []

for argv in sys.argv:
    argument.append(argv)

for args in argument:
    if(args.startswith('-')):
        flags = split(args)

#------------------------------------------------------------------------------
# Helper
#------------------------------------------------------------------------------
if('h' in flags):
    print("This is the helper! Soon there will be a lot of information here.")

#------------------------------------------------------------------------------
# Initialize Logger
#------------------------------------------------------------------------------
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Look for flags
if('f' in flags or 'L' in flags):
    if(not os.path.exists("log/")):
        os.makedirs("log/")
    now = datetime.now()
    logging.basicConfig(filename='log/pytom-log-%s.log' % now.strftime("%d_%m_%Y-%H:%M:%S"), level=logging.DEBUG, format="%(asctime)s-[%(levelname)s]: %(message)s")

if('l' in flags or 'L' in flags):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s-[%(levelname)s]: %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root.addHandler(handler)

if("file-logging" in argument or "console-logging" in argument):
    logging.info("Test Information message: This messages will inform about what the program is doing.")
    logging.warning("Test warning message: This messages will advise you about something.")
    logging.error("Test error message: This messages will inform about problems while executing the program.")
    logging.critical("Test critical message: This messages will inform about major problems in the program that may interrumpt it.")
    logging.debug("Test debug message: This messages are for the programmers, it will display some useful information.")