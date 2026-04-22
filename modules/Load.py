import os
import pandas as pd
import mysql.connector


def save_dataframe_to_csv(dataframe, output_dir, source_file_path):
    os.makedirs(output_dir, exist_ok=True)

    original_filename = os.path.basename(source_file_path)
    output_filename = "transformed_" + original_filename
    output_path = os.path.join(output_dir, output_filename)

    if hasattr(dataframe, "toPandas"):
        pandas_df = dataframe.toPandas()
    else:
        pandas_df = dataframe

    pandas_df.to_csv(output_path, index=False)

    print(f"CSV saved to {output_path}")
    return output_path


def map_pandas_dtype_to_mysql(dtype):
    dtype_str = str(dtype)

    if "int" in dtype_str:
        return "INT"
    elif "float" in dtype_str:
        return "DOUBLE"
    else:
        return "VARCHAR(255)"


def save_dataframe_to_mysql(dataframe, host, user, password, database, table_name):
    if hasattr(dataframe, "toPandas"):
        pandas_df = dataframe.toPandas()
    else:
        pandas_df = dataframe

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    cursor.close()
    connection.close()

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    column_defs = []
    for column_name, dtype in pandas_df.dtypes.items():
        mysql_type = map_pandas_dtype_to_mysql(dtype)
        column_defs.append(f"`{column_name}` {mysql_type}")

    create_table_sql = f"""
    CREATE TABLE {table_name} (
        {', '.join(column_defs)}
    )
    """
    cursor.execute(create_table_sql)

    columns_sql = ", ".join([f"`{col}`" for col in pandas_df.columns])
    placeholders = ", ".join(["%s"] * len(pandas_df.columns))
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"

    rows = [tuple(row) for row in pandas_df.itertuples(index=False, name=None)]
    cursor.executemany(insert_sql, rows)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Data saved to MySQL table {database}.{table_name}")