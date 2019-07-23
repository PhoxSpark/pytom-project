"""
Testing module
"""
import unittest
from .general_functions import split, save_obj, load_obj
from .flask_pack.pdb_dictionary_statements import PdbDictionaryStatements
from .flask_pack.pytom_database import make_url, download_url


class GeneralFunctionsTest(unittest.TestCase):
    """
    Test general functions
    """
    def test_split(self):
        """
        Testing split function
        """
        word = "Test"
        word = split(word)
        self.assertEqual(len(word), 4)

    def test_save_load_obj(self):
        """
        Testing save and load object functions
        """
        object_to_save = {"Test": "This is a test"}
        save_obj(object_to_save, "test")
        object_to_load = load_obj("test")
        self.assertEqual(object_to_save.items(), object_to_load.items())
        self.assertEqual(object_to_save, object_to_load)

def init_dict1():
    """
    Initialize test dictionary 1 for teststing.
    """
    dictionary = PdbDictionaryStatements()
    dictionary.pdb_dict = {"2ki5": {"ATOM": {"1": {"x": 1.0, "organism": "2ki5"}, \
    "2": {"x": 2.0, "organism": "2ki5"}, "3": {"x": 10.0, "organism": "2ki5"}}}}
    return dictionary

def init_dict2():
    """
    Initialize test dictionary 2 for teststing.
    """
    dictionary = PdbDictionaryStatements()
    dictionary.pdb_dict = {"2ki5": {"ATOM": {"1": {"x": 1.0, "organism": "2ki5"}, \
    "2": {"x": 2.0, "organism": "2ki5"}, "3": {"x": 10.0, "organism": "2ki5"}}}, \
    "1ki5": {"ATOM": {"1": {"x": 1.0, "organism": "2ki5"}, "2": {"x": 2.0, \
    "organism": "2ki5"}, "3": {"x": 10.0, "organism": "2ki5"}}}}
    return dictionary

class PDBDictionaryStatementsTest(unittest.TestCase):
    """
    Testing dictionary class and statements.
    """
    def test_select_camps(self):
        """
        Test select camps function
        """
        dictionary = init_dict1()
        dictionary.organism_list_add("2ki5")
        dictionary.select_camps([1.0], "x")
        self.assertIsNotNone(dictionary.pdb_dict)

    def test_select_range(self):
        """
        Test select a range of camps
        """
        dictionary = init_dict1()
        dictionary.organism_list_add("2ki5")
        dictionary.select_range([0.0, 20.0], "x")
        self.assertIsNotNone(dictionary.pdb_dict)

    def test_select_no_accurate(self):
        """
        Test select non accurate
        """
        dictionary = init_dict1()
        dictionary.organism_list_add("2ki5")
        dictionary.select_no_accurate([1], "x")
        self.assertIsNotNone(dictionary.pdb_dict)

    def test_rollback(self):
        """
        Test rollback
        """
        dictionary = init_dict2()
        dictionary.organism_list_add("2ki5")
        dictionary.select_camps([1.0], "x")
        dictionary.rollback(True)
        self.assertEqual(len(dictionary.pdb_dict), 2)

class PytomDatabaseTest(unittest.TestCase):
    """
    Testing download and make URL
    """
    def test_make_url(self):
        """
        Testing the creation of the URL
        """
        self.assertEqual(make_url(), "https://files.rcsb.org/download/2ki5.pdb")

    def test_download_url(self):
        """
        Testing the download of the URL.
        """
        test_download = download_url("name_", "Pytom_Downloads_Test", \
        "https://files.rcsb.org/download/2ki5.pdb", "2ki5")
        self.assertEqual(test_download, (False, "Pytom_Downloads_Test/name_2ki5.pdb"))
