import json
import os
import csv
import pandas as pd
import datetime

class CSVParquetHandler:
    def read_csv(self, file_path, standardize_dates=True):
        """
        Reads a CSV file and returns the headers and data.

        Args:
            file_path (str): Path to the CSV file.
            standardize_dates (bool, optional): Whether to standardize date fields to ISO format. Defaults to True.

        Returns:
            tuple: A tuple containing headers (list) and data (list of dictionaries).
        """
        with open(file_path, 'r') as csv_file:
            try:
                has_header = csv.Sniffer().has_header(csv_file.read(10024))
            except csv.Error:
                print(f"Could not sniff header for file {file_path}. Defaulting to no header.")
                has_header = False
            csv_file.seek(0)
            if has_header:
                data = list(csv.DictReader(csv_file))
                headers = data[0].keys()
            else:
                # Read the schema from the JSON file
                schema_file_path = os.path.splitext(file_path)[0] + '.json'
                with open(schema_file_path, 'r') as schema_file:
                    schema = json.load(schema_file)
                    headers = list(schema.keys())
                    data = list(csv.DictReader(csv_file, fieldnames=headers))

                # Handle extra fields in the JSON file schema
                for row in data:
                    for header in row.keys():
                        if header not in headers:
                            print(f"Warning: Extra field '{header}' found in the data.")

                # Handle missing fields in the JSON file schema
                for header in headers:
                    if header not in row:
                        print(f"Warning: Missing field '{header}' in the data.")

            # Standardize date fields to ISO format
            if standardize_dates:
                for row in data:
                    for header in headers:
                        if 'date' in header.lower():
                            try:
                                original_date = row[header]
                                standardized_date = self.standardize_date(original_date)
                                row[header] = standardized_date
                            except KeyError:
                                pass

            return headers, data

    def standardize_date(self, date_str):
        """
        Converts a date string to ISO format (yyyy-MM-dd).

        Args:
            date_str (str): Original date string.

        Returns:
            str: Date string in ISO format.
        """
        try:
            # Parse the original date using the expected format
            original_date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
            # Convert to ISO format
            standardized_date = original_date.strftime('%Y-%m-%d')
            return standardized_date
        except ValueError:
            # Handle invalid date formats gracefully
            print(f"Invalid date format: {date_str}")
            return date_str


class FileHandler:
    def __init__(self, input_directory, output_directory, csv_handler):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.csv_handler = csv_handler

    def process_files(self, output_format='csv'):
        """
        Process CSV files and write data to the specified output format.

        Args:
            output_format (str, optional): Output format ('csv' or 'parquet'). Defaults to 'csv'.
        """
        file_paths = [os.path.join(self.input_directory, file) for file in os.listdir(self.input_directory) if file.endswith('.csv')]
        for file_path in file_paths:
            headers, data = self.csv_handler.read_csv(file_path, standardize_dates=True)  # Optionally standardize dates
            # Process data here (you can customize this part)

            # Example: Print the headers and first few rows of data
            print(f"File: {file_path}")
            print("Headers:", headers)
            for row in data[:5]:
                print(row)

            # Write data to the specified output format
            file_name = os.path.basename(file_path)
            if output_format.lower() == 'csv':
                self.write_csv(data, headers, self.output_directory, file_name)
            elif output_format.lower() == 'parquet':
                self.write_parquet(data, headers, self.output_directory, file_name)
            elif output_format.lower() == 'csv|parquet':
                self.write_csv(data, headers, self.output_directory, file_name)
                self.write_parquet(data, headers, self.output_directory, file_name)
            else:
                print(f"Unsupported output format: {output_format}")

    def write_csv(self, data, headers, output_directory, file_name):
        csv_output_path = os.path.join(output_directory, file_name)
        with open(csv_output_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV file written: {csv_output_path}")

    def write_parquet(self, data, headers, output_directory, file_name):
        parquet_output_path = os.path.join(output_directory, os.path.splitext(file_name)[0] + '.parquet')
        df = pd.DataFrame(data, columns=headers)
        df.to_parquet(parquet_output_path, index=False)
        print(f"Parquet file written: {parquet_output_path}")


# Example usage
input_dir = "/Users/iswaryamogalapalli/PycharmProjects/dv01/input_csv_without_header/"
output_dir = "/Users/iswaryamogalapalli/PycharmProjects/dv01/output_path"
csv_reader = CSVParquetHandler()  # Initialize your CSVReader instance
file_handler = FileHandler(input_dir, output_dir, csv_reader)
file_handler.process_files(output_format='csv|parquet')  # Specify 'csv' or 'parquet'