import sys, logging, os
sys.path.append(".")
import pytomproject.flask_pack.flask_main as flask_main

#-----------------Log block-------------------
if(not os.path.exists):
    os.makedirs("logs/")
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO)
#---------------------------------------------

def main():
    logging.debug("Pytom initialized")
    logging.info("Starting Flask Framework")
    try:
        pass
        flask_main.run_flask()
    except Exception:
        logging.error("Can't initialize Flask, no more information obtained.")
    
if __name__ == '__main__':
    main()
