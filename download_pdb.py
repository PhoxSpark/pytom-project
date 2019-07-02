import urllib.request
import os

def question_y_n(question):
    """
    Send them an answer and it will return a 'y' or 'n'. It will not 
    continue with answers differents than Yes or No. It only takes 
    the user answer first character and make it lower for return and 
    testing.
    """
    answer = ''
    while(answer != 'n' and answer != 'y'):
        print(question)
        answer = input("Yes (y) or no (n): ")
        answer = str(answer[0]).lower()
        print(answer)
    return answer


def set_name_and_download_url():
    """
    Set and create download URL and return a tupla with the url and the 
    pdb name (the name can be whatever the user want, is for the file).
    """
    answer = question_y_n("Do you want to set a custom URL? ")
    if(answer == 'y'):
        url = input("URL Has to be something like: https://files.rcsb.org/download/ \n").lower()
        if(url[-1] != '/'):
            url += '/'
    else:
        url = "https://files.rcsb.org/download/"

    pdb_entry = str(input("Enter the entry of the organism (Ex: 2KI5): ")).lower()
    pdb_name = str(input("Enter the name for the file (Ex: herpesvirus1): ")).lower() + ".pdb"
    url += pdb_entry + ".pdb"

    return url, pdb_name

def download_pdb(url, pdb_name):
    """
    Take the url and pdb_name for download the file with custom name on
    a concrete location. Better to not change the location because the
    program will need this file to have it located but it can be changed
    directly on this function.
    """
    pdb_save_directory = "data/downloads/"

    print("Checking if directory exists...")
    if(os.path.exists(pdb_save_directory)):
        print("Directory %s exist." % pdb_save_directory)
    else:
        print("Making directory...")
        try:
            os.makedirs(pdb_save_directory)
        except OSError:
            print("Creation of the directory %s failed" % pdb_save_directory)
        else:
            print("Successfully created the directory %s" % pdb_save_directory)
    
    if(os.path.exists(pdb_save_directory + pdb_name)):
        print("File %s alredy exist! It will be overwrited." % pdb_name)
        answer = question_y_n("Do you want to continue?")
        if(answer == 'n'):
            exit
    else:
        print("File %s don't exist, it will be created." % pdb_name)

    pdb_save_directory = pdb_save_directory + pdb_name
    
    print("Beginning file download...")
    try:
        urllib.request.urlretrieve(url, pdb_save_directory)
    except ValueError:
        print("Download of %s failed." % url)
    else:
        print("File downloaded correctly on %s" % pdb_save_directory)


url, pdb_name = set_name_and_download_url()
download_pdb(url, pdb_name)
