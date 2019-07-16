import sys, logging, os
sys.path.append(".")
import pytomproject.flask_pack.run_flask as run_flask
import pytomproject.flask_pack.general_functions as general_functions

from pytomproject.flask_pack import db

def main():
    try:
        run_flask.start()
    except Exception:
        logging.error("Can't initialize Flask, no more information obtained.")

if __name__ == '__main__':
    main()
