import sys, logging, os
sys.path.append(".")
import pytomproject.flask_pack.flask_main as flask_main
import pytomproject.general_functions as general_functions

argument = []
for argv in sys.argv:
    argument.append(argv)

def main():
    general_functions.initialize_logger(argument)
    try:
        flask_main.run_flask()
    except Exception:
        logging.error("Can't initialize Flask, no more information obtained.")
    
if __name__ == '__main__':
    main()
