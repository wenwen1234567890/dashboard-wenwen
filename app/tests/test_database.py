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

    def test_get_ACT(self):
        """Test that the average ACT cost returns the correct value"""
        self.assertEquals(self.db_mod.get_avg_ACT(), 76.22)

    def test_get_max_quantity_prescribing(self):
        """Test that the max quantity prescribing returns the correct value"""
        self.assertEquals(
            self.db_mod.get_max_quantity_prescribing(), 10.58)

    def test_get_count_prescrib(self):
        """Test that the count prescrib returns the correct value"""
        self.assertEquals(self.db_mod.get_count_prescrib(), 791341)


if __name__ == "__main__":
    unittest.main()
