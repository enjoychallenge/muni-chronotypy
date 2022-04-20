import logging
import csv
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Let's convert raw data.")
    # Put needed files from https://drive.google.com/drive/folders/1ly6ypgG6LG3fiLFmBDLnCrJNb_XK40ay?usp=sharing to data/raw
    input_dir = 'data/raw/'
    input_file = 'all_rows_all_columns.csv'
    output_dir = 'data/derived/'
    output_full_file = 'all_rows_important_columns.csv'
    output_train_file = 'train_rows_important_columns.csv'
    input_path = os.path.join(input_dir, input_file)
    output_array = list()
    train_array = list()
    indices = [0, 3, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
               57, 59, 63, 66, 83, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
               111, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
    with open(input_path) as csv_file:
        csv_input = csv.reader(csv_file, delimiter=',')
        for row in csv_input:
            small_row = [row[idx] for idx in indices]
            output_array.append(small_row)
            if row[124] and row[124].strip():
                train_array.append(small_row)
    for file_name, source_array in [
        (output_full_file, output_array),
        (output_train_file, train_array),
    ]:
        with open(os.path.join(output_dir, file_name), mode='w') as output_file:
            output_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in source_array:
                output_csv.writerow(row)

    logger.info(f'Resume: len(small_csv)={len(output_array)}, len(train_csv)={len(train_array)}')
    logger.info(f'\tlen(small_csv)={len(output_array[0])}, len(train_csv)={len(train_array[0])}')

