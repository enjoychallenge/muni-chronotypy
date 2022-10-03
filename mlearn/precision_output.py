import os
import csv


DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(DIRECTORY, 'precision.csv')

def prepare_csv_output():
    with open(FILE_PATH, 'w', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        precision_writer.writerow(['Prediction_type', 'Area', 'Result_type', 'Model_name', 'Precision', 'Standard_deviation'])


def output_precision(prediction_type, area, cross_val_results, final_model):
    with open(FILE_PATH, 'a', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for name, _, mean, std in cross_val_results:
            precision_writer.writerow([prediction_type, area, 'cross_validation', name, mean, std, ])
        precision_writer.writerow([prediction_type, area, 'accuracy', final_model[0], final_model[-1], 0, ])
