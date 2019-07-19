import sys, logging, os
sys.path.append(".")
import pytomproject.flask_pack.run_flask as run_flask
import pytomproject.general_functions as general_functions
from pytomproject.flask_pack import db

def main():
    logging.info("Pytom initialized...")
    logging.info("Flask will be initialized...")
    run_flask.start()

if __name__ == '__main__':
    main()
