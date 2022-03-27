from config import ZNO_RESULTS_TABLE


def calculate_rows_to_skip_by_year_query(year):
    return f'''SELECT COUNT(*) FROM {ZNO_RESULTS_TABLE} WHERE year = {year};'''


def create_zno_results_table_query():
    return f'''
    CREATE TABLE IF NOT EXISTS {ZNO_RESULTS_TABLE}
    (
        id     VARCHAR(36) NOT NULL PRIMARY KEY,
        region VARCHAR(64) NULL,
        status VARCHAR(32) NULL,
        score  REAL NULL,
        year   INTEGER NULL
    );'''


def compare_max_results_by_region_and_year_query():
    return f'''
    SELECT region, year, MAX(score) as max_score
    FROM {ZNO_RESULTS_TABLE} 
    WHERE status='Зараховано' 
    GROUP BY region, year 
    ORDER BY region;'''
