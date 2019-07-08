import sys
sys.path.append(".")
import pytomproject.functions_classes as functions_classes
import pytomproject.flask_pack.flask_main as flask_main

def main():
    print("Pytom initialized.")
    pdb = functions_classes.Object_PDB()


if __name__ == '__main__':
    main()
