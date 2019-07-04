import os
import pytomproject.download_pdb as download_pdb

class Dictionary_PDB:

    pdb_dict_atom = {}

    def __init__(self, file_name, save_location):

        items = ("Atom serial number", "Atom name", "Alternate location indicator", "Residue name", "Chain identifier", "Residue sequence number", "Code for insertion of residues", "X orthogonal Å coordinate", "Y orthogonal Å coordinate", "Z orthogonal Å coordinate", "Occupancy", "Temperature factor", "Segment identifier", "Element symbol")

        print("Dictionary creation initialized with the file %s" % file_name + ".pdb")

        with open(save_location + file_name + ".pdb") as f:
            content = f.readlines()
        
        for line in content:
            if(line.startswith("ATOM")):
                atom_type = line[12:15].strip(" ")
                atom_id = line[6:10].strip(" ")
                if(atom_type not in self.pdb_dict_atom):
                    self.pdb_dict_atom[atom_type][atom_id] = []
                self.pdb_dict_atom[atom_type][atom_id].append(line[6:10].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[12:15].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[16].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[17:19].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[21].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[22:25].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[26].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[30:37].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[38:45].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[46:53].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[54:59].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[60:65].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[72:75].strip(" "))
                self.pdb_dict_atom[atom_type][atom_id].append(line[76:77].strip(" ").strip("\n"))

        print(self.pdb_dict_atom["CG"])
                
