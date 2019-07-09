import sys
sys.path.append("..")
import unittest
from unittest.mock import patch
import pytomproject.functions_classes as functions_classes

class Test_Class_PDB(unittest.TestCase):

    def test_class_pdb_initialization(self):
        """
        Test if the class it's correctly initialized with his atributes
        using te default inputs.
        """
        pdb = functions_classes.Object_PDB()
        self.assertEqual(pdb.organism, "2ki5")
        self.assertEqual(pdb.name, "downloaded_pdb.pdb")
        self.assertEqual(pdb.url, "https://files.rcsb.org/download/2ki5.pdb")
        self.assertEqual(pdb.path, "Downloads")
        self.assertIsNotNone(pdb.pdb_dictionary)



class Test_User_Prompt(unittest.TestCase):

    @patch('builtins.input', return_value='yes')
    def test_question_y(self, input):
        answer = functions_classes.question_y_n("Are you clever?")
        self.assertEqual(answer, 'y')
    
    @patch('builtins.input', return_value='NO')
    def test_question_n(self, input):
        answer = functions_classes.question_y_n("Are you dumb?")
        self.assertEqual(answer, 'n')
        
