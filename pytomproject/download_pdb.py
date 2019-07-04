import urllib.request
import os
import pytomproject.user_prompt as pytomproject

def make_url(url_no_file = "https://files.rcsb.org/download/", organism_entry = "2ki5"):
    """
    Takes the download URL without the file of the PDB database and the organism entry 
    and converts it in to a download link for the PDB file.

    Returns the full URL for download.
    """
    print("Making URL...")
    url = url_no_file + organism_entry + ".pdb"
    print("Url %s created." % url)

    return url
    
def download_url(url = None, pdb_name = "downloaded_pdb", pdb_save_location = "~/.PytomProject/Downloads"):
    """
    Receive the url, file name and save location and download the file of the url called
    "pdb_name" and saves it on "pdb_save_location".

    Return True if the download was successful and False if it wasn't.
    """


    print("Checking if directory exists...")
    if(os.path.exists(pdb_save_location)):
        print("Directory %s exist." % pdb_save_location)
    else:
        print("Directory %s don't exists, creating it..." % pdb_save_location)
        try:
            os.makedirs(pdb_save_location)
        except OSError:
            print("Creation of the directory %s failed" % pdb_save_location)
        else:
            print("Successfully created the directory %s" % pdb_save_location)

    print("Creating download path")

    print("Beginning file download...")
    try:
        urllib.request.urlretrieve(url, pdb_save_location + pdb_name + ".pdb")
    except ValueError:
        print("Download of %s failed." % url)
        downloaded = False
    else:
        print("File downloaded correctly on %s" % pdb_save_location)
        downloaded = True

    return downloaded    
