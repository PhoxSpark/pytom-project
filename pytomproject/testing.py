import unittest
from unittest.mock import patch
import pytomproject.download_pdb as download_pdb
import pytomproject.user_prompt as user_prompt

class TestDownload_pdbPDB(unittest.TestCase):

    def test_make_url(self):
        organism_entry = "2ki5"
        url_no_file = "https://files.rcsb.org/download/"
        url1 = download_pdb.make_url()
        url2 = download_pdb.make_url(url_no_file, organism_entry)
        self.assertEqual(url1, url2)
        self.assertEqual(url1, url_no_file+organism_entry+".pdb")
    
    def test_download_pdb_pdb(self):
        url = "https://files.rcsb.org/download/2ki5.pdb"
        self.assertTrue(download_pdb.download_url(url))

class TestUserPrompt(unittest.TestCase):

    @patch('builtins.input', return_value='yes')
    def test_question_y(self, input):
        answer = user_prompt.question_y_n("Are you clever?")
        self.assertEqual(answer, 'y')
    
    @patch('builtins.input', return_value='NO')
    def test_question_n(self, input):
        answer = user_prompt.question_y_n("Are you dumb?")
        self.assertEqual(answer, 'n')
        
