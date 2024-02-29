import unittest
from unittest.mock import patch
import csv
import json
import itertools
from unittest.mock import patch, mock_open
from dv01_de_challenge import CSVHandler


class TestCSVHandler(unittest.TestCase):

    def test_read_csv_with_header(self):
        file_path = '/input_csv/LoanStats_securev1_2018Q4.csv'  # Path to a CSV file with a header
        expected_headers = list(
            csv.reader(open('/input_csv/LoanStats_securev1_2018Q4.csv')))[
            0]  # Read headers from actual file
        expected_data = [
            {'column1': 'value1', 'column2': 'value2'},
            {'column1': 'value3', 'column2': 'value4'}
        ]  # Expected data

        mocked_data = csv.writer(None, delimiter=',').writerows(expected_data)
        mocked_csv_content = '\n'.join(mocked_data)

        with patch('builtins.open', mock_open(read_data=mocked_csv_content)):
            csv_handler = CSVHandler()
            headers, data = csv_handler.read_csv(file_path)

        self.assertEqual(headers, expected_headers)
        self.assertEqual(data, expected_data)

    def test_read_csv_without_header_and_schema(self):
        file_path = '/input_csv_without_header/LoanStats_securev1_2018Q4.csv'  # Path to a CSV file without a header
        schema_file_path = '/input_csv_without_header/LoanStats_securev1_2018Q4.json'  # Path to the corresponding JSON schema file
        expected_headers = ['columnA', 'columnB']  # Expected headers from the schema
        expected_data = [
            {'columnA': 'value5', 'columnB': 'value6'},
            {'columnA': 'value7', 'columnB': 'value8'}
        ]  # Expected data

        with patch('builtins.open', mock_open(read_data=csv.reader(expected_data, delimiter=','))) as mock_csv_file:
            with patch('json.load', return_value={'header_row': expected_headers}):
                csv_handler = CSVHandler()
                headers, data = csv_handler.read_csv(file_path)

        mock_csv_file.assert_called_once_with(file_path, 'r')
        self.assertEqual(headers, expected_headers)
        self.assertEqual(data, expected_data)

    def test_write_csv(self):
        data = [
            {'column1': 'valueX', 'column2': 'valueY'},
            {'column1': 'valueZ', 'column2': 'value10'}
        ]
        headers = ['column1', 'column2']
        output_path = '/dv01_de_challenge/output_path/LoanStats_securev1_2018Q4.csv'

        with patch('builtins.open', mock_open()) as mock_csv_file:
            csv_handler = CSVHandler()
            csv_handler.write_csv(data, headers, output_path)

        mock_csv_file.assert_called_once_with(output_path, 'w', newline='')
        expected_csv_content = 'column1,column2\nvalueX,valueY\nvalueZ,value10\n'
        mock_csv_file().write.assert_called_once_with(expected_csv_content)
