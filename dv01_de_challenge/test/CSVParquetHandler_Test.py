import unittest
from unittest.mock import mock_open, patch
from dv01_de_challenge import CSVParquetHandler  # Replace with the actual module name

class TestCSVParquetHandler(unittest.TestCase):
    def setUp(self):
        self.handler = CSVParquetHandler()

    def test_read_csv_with_header(self):
        #  **Sample Data:**
        csv_content = """header1,header2
       value1,value2
       value3,value4
       value5,value with a comma,
       """

        with patch("builtins.open", mock_open(read_data=csv_content)):
            headers, data = self.handler.read_csv("test_data.csv")

        # Assertions
        self.assertEqual(headers, ["header1", "header2"])
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]["header1"], "value1")
        self.assertEqual(data[1]["header2"], "value4")
        self.assertEqual(data[3]["header2"], "")  # Handle values with commas

    def test_read_csv_without_header(self):
        #  **Sample Data:**
        csv_content = """value1,value2
       value3,value with comma
       value5,123
       """

        with patch("builtins.open", mock_open(read_data=csv_content)):
            headers, data = self.handler.read_csv("test_data.csv", standardize_dates=False)

        # Assertions
        self.assertEqual(headers, ["column1", "column2"])  # Assuming your schema keys
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["column1"], "value1")
        self.assertEqual(data[1]["column2"], "value with comma")
        self.assertTrue(isinstance(data[2]["column2"], int))  # Handle different data types
if __name__ == "__main__":
    unittest.main()