import unittest
import os
from dotenv import load_dotenv
import requests
from census_api import Search_Census


class TestAPI(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.api = "https://api.census.gov"
        self.census_key_name = "CENSUS_API_KEY"
        self.census_key = os.environ.get(self.census_key_name)
        self.tempPath = './'
        self.tempFilename = 'tempFileforTesting'
        self.pathToTemp = f'{self.tempPath}{self.tempFilename}.csv'

        return super().setUp()

    def test_key(self):
        self.assertIsNotNone(
            self.census_key, f"Please save an api key named: '{self.census_key_name}' in .env file in main directory.")

    def test_connection(self):
        self.assertEqual(requests.get(self.api).status_code,
                         200, f"Connection to {self.api} was not established.")

    def test_NewFile_incorrect_formatting(self):
        # incorrect search params
        with self.assertRaises(AssertionError):
            Search_Census(2300, 'pep/charagegroups', 'name')
        with self.assertRaises(AssertionError):
            Search_Census(2019, 'pep/charagegroups')

        # bad keyword definitions
        with self.assertRaises(ValueError):
            Search_Census(2005, 'pep/charagegroups',
                          'name', file_name='bad!filename')
        with self.assertRaises(ValueError):
            Search_Census(2005, 'pep/charagegroups',
                          'name', save_path='bad-path')

        # 200 return from bad url
        with self.assertRaises(ConnectionError):
            Search_Census(2005, 'pep/charagegroups', 'parmNotReal')

    def test_success(self):
        Search_Census(2019, 'pep/charagegroups', "name",
                      file_name=self.tempFilename, save_path=self.tempPath)
        succ = os.path.isfile(self.pathToTemp)
        self.assertTrue(succ)

    def tearDown(self) -> None:
        if os.path.isfile(self.pathToTemp):
            os.remove(self.pathToTemp)
        return super().tearDown()


if __name__ == "__main__":
    unittest.main(verbosity=2)
