from config import ZNO_RESULTS_TABLE


def write_zno_results(data, connection):
    columns = ",".join([str(i) for i in data.columns.tolist()])
    with connection.cursor() as cursor:
        for i, row in data.iterrows():
            sql = f'''INSERT INTO {ZNO_RESULTS_TABLE} ({columns}) 
            VALUES (
            '{row.get("id")}', 
            '{row.get("region")}', 
            '{row.get("status")}', 
            {row.get("score")}, 
            {row.get("year")});'''
            cursor.execute(sql, tuple(row))
            connection.commit()
