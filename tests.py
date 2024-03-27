import time
import unittest

import os
import pandas as pd
import sys

from requests.exceptions import HTTPError

# Add the path to the raw_data_getter package to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_getter import DataGetter


class TestDataGetter(unittest.TestCase):
    def setUp(self):
        time.sleep(2)  # API rate limit
        self.data_getter = DataGetter()

    #########################################################
    # ACCESS TOKEN
    #########################################################

    def test_get_access_token(self):
        data_getter = DataGetter(testing=True)
        self.assertEqual(data_getter.access_token, "test_token")

    def test_get_access_token_real_mode(self):
        self.assertNotEqual(self.data_getter.access_token, "test_token")
        self.assertTrue(isinstance(self.data_getter.access_token, str))

    def test_get_access_token_bad_client_id(self):
        self.data_getter.GOUV_API_CLIENT_ID = "bad_client_id"
        with self.assertRaises(HTTPError):
            self.data_getter.get_or_refresh_access_token()

    def test_get_access_token_bad_secret_key(self):
        data_getter = DataGetter()
        data_getter.GOUV_API_SECRET_KEY = "bad_secret_key"

        with self.assertRaises(HTTPError):
            data_getter.get_or_refresh_access_token()

    def test_get_access_token_bad_scopes(self):
        with self.assertRaises(HTTPError):
            self.data_getter.get_or_refresh_access_token(scopes=["bad_scope"])

    #########################################################
    # DATA FETCHING
    #########################################################

    def test_xml_to_dataframe(self):
        xml = """
            <root>
                <item>
                    <title>Item 1</title>
                    <description>Description 1</description>
                </item>
                <item>
                    <title>Item 2</title>
                    <description>Description 2</description>
                </item>
            </root>
        """
        df = DataGetter.to_dataframe(xml)
        self.assertEqual(df.shape, (2, 2))
    

    def test_get_job_seekers_of_last_12_months(self):
        job_seekers = self.data_getter.get_job_seekers_of_last_12_months()
        
        self.assertTrue(isinstance(job_seekers, pd.DataFrame))


if __name__ == "__main__":
    unittest.main()
