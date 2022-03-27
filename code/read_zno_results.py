import pandas as pd

from config import *


def read_zno_results(year, skip_rows):
    df = pd.read_csv(
        ZNO_RESULTS_YEAR_TO_FILE.get(year),
        skiprows=[i for i in range(1, skip_rows + 1)],
        usecols=ZNO_RESULTS_FILE_YEAR_TO_COLUMNS_TO_USE.get(year),
        # nrows=100,
        encoding=ZNO_RESULTS_YEAR_TO_ENCODING.get(year),
        sep=ZNO_RESULTS_FILE_SEPARATOR)
    df.columns = ["id", "region", "status", "score"]
    df["year"] = year
    df["score"] = df["score"].str.replace(",", ".")
    df["score"] = df["score"].fillna('null')
    return df
