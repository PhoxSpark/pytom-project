import pytomproject.flask_pack.flask_main as flask_main
import pytomproject.user_prompt as user_prompt

import pytomproject.download_pdb as download_pdb
import pytomproject.pdb_dictionary as pdb_dictionary

webgui = user_prompt.question_y_n("Do you want to use the web GUI?")
if(webgui == 'y'):
    pass
else:
    file_name = "testing"
    save_location = "Pytomproject/Downloads/"
    download_pdb.download_url(download_pdb.make_url(), file_name, save_location)
    pdb_data = pdb_dictionary.Dictionary_PDB(file_name, save_location)
