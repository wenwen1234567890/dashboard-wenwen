"""
NAME:          test_database.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          24/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Suite of tests for testing the dashboards database
               functionality.
"""

import unittest
#from app import app
from app.database.controllers import Database

class DatabaseTests(unittest.TestCase):
    """Class for testing database functionality and connection."""
    def setUp(self):
        """Run prior to each test."""
        self.db_mod = Database()

    def tearDown(self):
        """Run post each test."""
        pass

    def test_get_total_number_items(self):
        """Test that the total number of itmems returns the correct value."""
        self.assertEquals(self.db_mod.get_total_number_items(), 8218165)

    def test_avg_ACT(self):
        self.assertEquals(self.db_mod.get_avg_ACT() - 76.22065025148007 < 1e6, True)

    def test_max_quantity_prescribing(self):
        self.assertEquals(self.db_mod.get_max_quantity_prescribing(), 869879)

    def test_count_prescrib(self):
        self.assertEquals(self.db_mod.get_count_prescrib(), 791341)

    def test_get_treatment_percentage(self):
        treatment_percentage = self.db_mod.get_treatment_percentage()
        self.assertEquals(treatment_percentage, [82.25, 5.22, 2.68, 9.62, 0.23])



if __name__ == "__main__":
    unittest.main()
