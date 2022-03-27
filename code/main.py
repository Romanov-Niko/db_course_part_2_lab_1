import psycopg2
import time
import os
import logging

from csv import writer as csv_writer
from read_zno_results import *
from write_zno_results import *
from sql_queries import *
from config import *


def create_connection():
    return psycopg2.connect(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"]
    )

# def create_connection():
#     return psycopg2.connect(
#         user="postgres",
#         password="password",
#         dbname="test",
#         host="localhost",
#         port="5433"
#     )


def execute_query(connection, sql_query):
    buffer = list()
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        if cursor.description is not None:
            for row in cursor:
                buffer.append(tuple(map(lambda x: x.strip() if type(x) is str else x, row)))
    return None if len(buffer) == 0 else buffer


def save_result_in_csv(data: list):
    os.makedirs(os.path.dirname(RESULT_FILE_PATH), exist_ok=True)
    with open(RESULT_FILE_PATH, 'w', encoding=RESULT_FILE_ENCODING) as f:
        file_writer = csv_writer(f, delimiter=RESULT_FILE_DELIMITER)
        file_writer.writerow(list(map(str, RESULT_FILE_HEADERS)))
        for element in data:
            file_writer.writerow(list(map(str, element)))


def save_results(connection, processing_time):
    os.makedirs(os.path.dirname(TIME_CONSUMPTION_FILE_PATH), exist_ok=True)
    with open(TIME_CONSUMPTION_FILE_PATH, "w") as text_file:
        text_file.write("Processing time in seconds: %s" % round(processing_time, 2))
    with connection as conn:
        results = execute_query(connection=conn, sql_query=compare_max_results_by_region_and_year_query())
    save_result_in_csv(results)


def main():
    logging.info("Start processing")
    connection = create_connection()
    with connection:
        execute_query(connection=connection, sql_query=create_zno_results_table_query())

    start = time.time()

    for year in ZNO_RESULTS_YEAR_TO_FILE.keys():
        logging.info("Processing of file: ", ZNO_RESULTS_YEAR_TO_FILE.get(year))
        with connection:
            imported_rows_number = \
                execute_query(connection=connection, sql_query=calculate_rows_to_skip_by_year_query(year))[0][0]
            zno_results = read_zno_results(year, imported_rows_number)
            write_zno_results(zno_results, connection)

    end = time.time()

    save_results(connection, end - start)

    connection.close()
    logging.info("Finish processing")

if __name__ == '__main__':
    main()
