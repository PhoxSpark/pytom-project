from . import functions_classes
from .flask_pack import flask_main
import logging, os, sys
from datetime import datetime

#-----------------Log block-----------------------------------------------------------------------------------------------------------


if(not os.path.exists("log/")):
    os.makedirs("log/")

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

now = datetime.now()

root = logging.getLogger()
root.setLevel(logging.DEBUG)
logging.basicConfig(filename='log/pytom-log-%s.log' % now.strftime("%d_%m_%Y-%H:%M:%S"), level=logging.DEBUG, format="%(asctime)s-[%(levelname)s]: %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s-[%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)
#-------------------------------------------------------------------------------------------------------------------------------------