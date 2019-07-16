import sys
sys.path.append("..")
import unittest
from unittest.mock import patch
from .general_functions import split, question_y_n, save_obj, load_obj
from .flask_pack.pdb_dictionary_statements import PDB_Dictionary_Statements
from .flask_pack.pytom_database import make_url, download_url, add_new_organism

class Test_User_Prompt(unittest.TestCase):

    @patch('builtins.input', return_value='yes')
    def test_question_y(self, input):
        answer = question_y_n("Are you clever?")
        self.assertEqual(answer, 'y')
    
    @patch('builtins.input', return_value='NO')
    def test_question_n(self, input):
        answer = question_y_n("Are you dumb?")
        self.assertEqual(answer, 'n')
        

class General_Functions_Test(unittest.TestCase):

    def test_split(self):
        word = "Test"
        word = split(word)
        self.assertEqual(len(word), 4)
    
    def test_save_load_obj(self):
        object_to_save = {"Test": "This is a test"}
        save_obj(object_to_save, "test")
        object_to_load = load_obj("test")
        self.assertEqual(object_to_save.items(), object_to_load.items())
        self.assertEqual(object_to_save, object_to_load)

def init_dict1():
    dictionary = PDB_Dictionary_Statements()
    dictionary.pdb_dict = {"2ki5": {"ATOM": {"1": {"x": 1.0, "organism": "2ki5"}, "2": {"x": 2.0, "organism": "2ki5"}, "3": {"x": 10.0, "organism": "2ki5"}}}}
    return dictionary

def init_dict2():
    dictionary = PDB_Dictionary_Statements()
    dictionary.pdb_dict = {"2ki5": {"ATOM": {"1": {"x": 1.0, "organism": "2ki5"}, "2": {"x": 2.0, "organism": "2ki5"}, "3": {"x": 10.0, "organism": "2ki5"}}}, "1ki5": {"ATOM": {"1": {"x": 1.0, "organism": "2ki5"}, "2": {"x": 2.0, "organism": "2ki5"}, "3": {"x": 10.0, "organism": "2ki5"}}}}
    return dictionary

class PDB_Dictionary_Statements_Test(unittest.TestCase):

    def test_select_camps(self):
        dictionary = init_dict1()
        dictionary.select_camps([1.0], "x", ["2ki5"])
        self.assertIsNotNone(dictionary.pdb_dict)
    
    def test_select_range(self):
        dictionary = init_dict1()
        dictionary.select_range([0.0, 20.0], "x", ["2ki5"])
        self.assertIsNotNone(dictionary.pdb_dict)
    
    def test_select_no_accurate(self):
        dictionary = init_dict1()
        dictionary.select_no_accurate([1], "x", ["2ki5"])
        self.assertIsNotNone(dictionary.pdb_dict)
    
    def test_rollback(self):
        dictionary = init_dict2()
        dictionary.select_camps([1.0], "x", ["2ki5"])
        dictionary.rollback(True)
        self.assertEqual(len(dictionary.pdb_dict), 2)

class Pytom_Database_Test(unittest.TestCase):

    def test_make_url(self):
        self.assertEqual(make_url(), "https://files.rcsb.org/download/2ki5.pdb")
    
    def test_download_url(self):
        test_download = download_url("name_", "Pytom_Downloads_Test", "https://files.rcsb.org/download/2ki5.pdb", "2ki5")
        self.assertEqual(test_download, (False, "Pytom_Downloads_Test/name_2ki5.pdb"))
