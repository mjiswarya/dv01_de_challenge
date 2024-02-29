import csv
import os
import json

class CSVHandler:
    def __init__(self):
        pass

    def read_csv(self, file_path):
        # Read the first line of the CSV file
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
        return headers, data

    def write_csv(self, data, headers, output_directory, file_name):
        output_path = os.path.join(output_directory, file_name)
        with open(output_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

class FileHandler:
    def __init__(self, input_directory, output_directory, csv_handler):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.csv_handler = csv_handler

    def process_files(self):
        file_paths = [os.path.join(self.input_directory, file) for file in os.listdir(self.input_directory) if file.endswith('.csv')]
        for file_path in file_paths:
            headers, data = self.csv_handler.read_csv(file_path)
            # Process data here
            file_name = os.path.basename(file_path)
            self.csv_handler.write_csv(data, headers, self.output_directory, file_name)

csv_handler = CSVHandler()
file_handler = FileHandler('/Users/iswaryamogalapalli/PycharmProjects/dv01/input_csv/', '/Users/iswaryamogalapalli/PycharmProjects/dv01/output_path', csv_handler)
file_handler.process_files()