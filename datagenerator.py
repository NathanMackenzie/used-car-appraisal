from csv import DictReader, writer
import numpy as np
import pandas as pd
import logging


class DataGenerator:
    def __init__(self, input_path, output_path, categories, features, labels):
        self.input_path = input_path
        self.output_path = output_path
        self.categories = categories
        self._features = features
        self._labels = labels

        self.reduce_data()

    def reduce_data(self):
        logging.info("Preparing data...")
        
        # Open output file
        with open(self.output_path, 'w', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(self.categories)

            # Read input file row-by-row
            with open(self.input_path, 'r', encoding="utf8") as read_obj:
                csv_reader = DictReader(read_obj)

                for i, row in enumerate(csv_reader):
                    try:
                        if self.is_row_valid(row):
                            output_row = [row['price'], row['year'], row['manufacturer'], row['model'], row['condition'], row['odometer']]
                            csv_writer.writerow(output_row)
                    except UnicodeDecodeError:
                        logging.warn("Unable to decode a row")


    def load_data(self):
        raw_data = pd.read_csv(self.output_path)
        train_features = pd.DataFrame()
        train_labels = pd.DataFrame()

        for i, cat in enumerate(self.categories):
            train_features.insert(i, cat, raw_data.pop(cat))

        for i, label in enumerate(self._labels):
            train_labels.insert(i, label, train_features.pop(label))

        return np.array(train_features), np.array(train_labels)

    def is_row_valid(self, row):
        # Check that all fields have a value
        for value in row.values():
            if value == '':
                return False

        # Check that manufacturer is valid
        for man in self._features[0].keys():
            if(man == row.get('manufacturer')):
                # Check that model is valid
                for model in self._features[0].get(man):
                    if(model in row.get('model')):
                        row['model'] = model
                        return True
        return False

