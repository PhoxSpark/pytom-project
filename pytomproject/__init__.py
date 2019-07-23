"""
Initialization of pytomproject package.
"""
import os
import logging
import sys
from datetime import datetime
from .general_functions import split
from .flask_pack import run_flask

#------------------------------------------------------------------------------
# Take ARGUMENTs
#------------------------------------------------------------------------------
ARGUMENT = []
FLAGS = []

for argv in sys.argv:
    ARGUMENT.append(argv)

for args in ARGUMENT:
    if args.startswith('-'):
        FLAGS = split(args)

#------------------------------------------------------------------------------
# Initialize Logger
#------------------------------------------------------------------------------
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Look for flags
if 'L' in FLAGS:

    if not os.path.exists("log/"):
        os.makedirs("log/")

    NOW = datetime.now()
    logging.basicConfig(filename='log/pytom-log-%s.log' % NOW.strftime("%d_%m_%Y-%H:%M:%S"), \
    level=logging.DEBUG, format="%(asctime)s-[%(levelname)s]: %(message)s")

if 'l' in FLAGS:
    ROOT = logging.getLogger()
    ROOT.setLevel(logging.DEBUG)
    FORMATTER = logging.Formatter("%(asctime)s-[%(levelname)s]: %(message)s")
    HANDLER = logging.StreamHandler(sys.stdout)
    HANDLER.setLevel(logging.INFO)
    HANDLER.setFormatter(FORMATTER)
    ROOT.addHandler(HANDLER)

if("file-logging" in ARGUMENT or "console-logging" in ARGUMENT):
    logging.info("Test Information message: This messages will inform about what \
    the program is doing.")
    logging.warning("Test warning message: This messages will advise you about \
    something.")
    logging.error("Test error message: This messages will inform about problems \
    while executing the program.")
    logging.critical("Test critical message: This messages will inform about major \
    problems in the program that may interrumpt it.")
    logging.debug("Test debug message: This messages are for the programmers, \
    it will display some useful information.")

#------------------------------------------------------------------------------
# Helper
#------------------------------------------------------------------------------
if 'h' in FLAGS:

    with open("README.md", 'r') as fin:
        print(fin.read())
        sys.exit()
