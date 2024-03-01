import unittest
from unittest.mock import patch
import csv
import json
import itertools
from unittest.mock import patch, mock_open
from dv01_de_challenge import CSVHandler as ch

class TestCSVHandler(unittest.TestCase):

    def test_read_csv_with_header(self):
        # Sample CSV data with header
        csv_content = """id,member_id,loan_amnt
        100001,12345,10000
        100002,54321,20000"""

        with patch("builtins.open", mock_open(read_data=csv_content)):
            csv_handler = ch.CSVHandler()
            headers, data = csv_handler.read_csv("test_data.csv")

        # Expected output
        expected_headers = ["id", "member_id", "loan_amnt"]
        expected_data = [
            {"id": "100001", "member_id": "12345", "loan_amnt": "10000"},
            {"id": "100002", "member_id": "54321", "loan_amnt": "20000"},
        ]

        self.assertEqual(headers, expected_headers)
        self.assertEqual(data, expected_data)

    def test_read_csv_without_header_and_schema(self):
        # Sample CSV data without header
        csv_content = """value1,value2
        value3,value4"""

        with patch("builtins.open", mock_open(read_data=csv_content)):
            with patch("json.load", return_value={"header_row": ["columnA", "columnB"]}):
                csv_handler = ch.CSVHandler()
                headers, data = csv_handler.read_csv("test_data.csv")

        # Expected output
        expected_headers = ["columnA", "columnB"]
        expected_data = [
            {"columnA": "value1", "columnB": "value2"},
            {"columnA": "value3", "columnB": "value4"},
        ]

        self.assertEqual(headers, expected_headers)
        self.assertEqual(data, expected_data)

    def test_write_csv(self):
        # Sample data and headers
        data = [
            {"column1": "valueX", "column2": "valueY"},
            {"column1": "valueZ", "column2": "value10"},
        ]
        headers = ["column1", "column2"]

        # Mocking file write
        with patch("builtins.open", mock_open()) as mock_csv_file:
            csv_handler = ch.CSVHandler()
            csv_handler.write_csv(data, headers, "output.csv")

        # Expected CSV content
        expected_csv_content = "column1,column2\nvalueX,valueY\nvalueZ,value10\n"
        mock_csv_file().write.assert_called_once_with(expected_csv_content)

if __name__ == "__main__":
    unittest.main()
