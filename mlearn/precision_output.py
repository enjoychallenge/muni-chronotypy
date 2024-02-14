import os
import csv


DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(DIRECTORY, 'precision.csv')


def prepare_csv_output():
    with open(FILE_PATH, 'w', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        precision_writer.writerow(['Prediction_type', 'Result_type', 'Model_name', 'Neg Root Mean Squared Error - avg', 'Root Mean Squared Error - std dev'])


def output_precision(pred_col_names, cross_val_results, final_model):
    prediction_name = '+'.join(pred_col_names)
    with open(FILE_PATH, 'a', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for name, _, rmse, stdev in cross_val_results:
            precision_writer.writerow([prediction_name, 'cross_validation', name, rmse, stdev ])
        precision_writer.writerow([prediction_name, 'Neg root mean squared error', final_model[0], final_model[-1], 0, ])
