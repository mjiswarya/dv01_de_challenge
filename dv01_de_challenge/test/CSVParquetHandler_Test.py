import unittest
from unittest.mock import mock_open, patch
from dv01_de_challenge import CSVParquetHandler  # Replace with the actual module name

class TestCSVParquetHandler(unittest.TestCase):
    def setUp(self):
        self.handler = CSVParquetHandler()

    def test_read_csv_with_header(self):
        # Mock the CSV file content
        csv_content = "header1,header2\nvalue1,value2\nvalue3,value4"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            headers, data = self.handler.read_csv("test_data.csv")

        # Assertions
        self.assertEqual(headers, ["header1", "header2"])
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["header1"], "value1")
        self.assertEqual(data[1]["header2"], "value4")

    def test_read_csv_without_header(self):
        # Mock the CSV file content without a header
        csv_content = "value1,value2\nvalue3,value4"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            headers, data = self.handler.read_csv("test_data.csv", standardize_dates=False)

        # Assertions
        self.assertEqual(headers, ["column1", "column2"])  # Assuming your schema keys
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["column1"], "value1")
        self.assertEqual(data[1]["column2"], "value4")

if __name__ == "__main__":
    unittest.main()
