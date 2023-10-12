import os
import csv
import settings
import psycopg2


DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(DIRECTORY, 'precision.csv')
STATS_FILE_PATH = os.path.join(DIRECTORY, 'stats.csv')


def prepare_csv_output():
    with open(FILE_PATH, 'w', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        precision_writer.writerow(['Prediction_type', 'Result_type', 'Model_name', 'Precision', 'Standard_deviation'])


def output_precision(prediction_type, cross_val_results, final_model):
    with open(FILE_PATH, 'a', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for name, _, mean, std in cross_val_results:
            precision_writer.writerow([prediction_type, 'cross_validation', name, mean, std, ])
        precision_writer.writerow([prediction_type, 'r2_score', final_model[0], final_model[-1], 0, ])


def output_stats():
    with open(STATS_FILE_PATH, 'w', newline='') as csvfile:
        precision_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        precision_writer.writerow(['File_id', 'Points count', 'Errors count', 'Errors count percentage', 'Average error'])
    export_stats_query = f'''COPY (with errors as (select file_id,
                           id,
                           heart_rate_avg_perc,
                           pred_heart_rate_avg_perc,
                           abs(heart_rate_avg_perc-pred_heart_rate_avg_perc) pred_error
                    from all_with_predictions)
    select file_id,
           count(*) cnt,
           count(case when pred_error = 0 then null else pred_error end) cnt_error,
           count(case when pred_error = 0 then null else pred_error end) * 100 / count(*) cnt_perc,
           ROUND(sum(pred_error) * 1000 / count(*)) / 1000 avg_error
    from errors
    group by file_id
    order by file_id asc) TO STDOUT WITH CSV DELIMITER ',' '''
    conn = psycopg2.connect(settings.PG_CONN)

    conn.autocommit = True
    cursor = conn.cursor()
    with open(STATS_FILE_PATH, 'a', newline='') as csvfile:
        cursor.copy_expert(export_stats_query, csvfile)

