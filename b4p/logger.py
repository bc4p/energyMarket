

import os
import csv
import pandas as pd

class DictLogger:
    def __init__(self, log_folder):
        self.log_folder = log_folder
        os.makedirs(log_folder, exist_ok=True)

    def log_dictionary(self, dictionary, filename):
        log_file_path = os.path.join(self.log_folder, filename + '.csv')
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=dictionary.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(dictionary)

    def read_csv_to_dataframe(self, filename):
        log_file_path = os.path.join(self.log_folder, filename + '.csv')
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"File '{filename}.csv' not found in the log folder.")
        
        df = pd.read_csv(log_file_path)
        return df
