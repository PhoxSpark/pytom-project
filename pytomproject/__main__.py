import sys, logging, os
sys.path.append(".")
import pytomproject.flask_pack.flask_main as flask_main

def main():
    logging.debug("******************************************************************")
    logging.debug("********************* Pytom initialized **************************")
    logging.debug("******************************************************************")
    logging.info("Starting Flask Framework")
    try:
        pass
        flask_main.run_flask()
    except Exception:
        logging.error("Can't initialize Flask, no more information obtained.")
    
if __name__ == '__main__':
    main()
