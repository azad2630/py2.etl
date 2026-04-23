import os
import pandas as pd
import mysql.connector
import modules.Security


def save_dataframe_to_csv(dataframe, output_dir, source_file_path):
    os.makedirs(output_dir, exist_ok=True)

    original_filename = os.path.basename(source_file_path)
    output_filename = "transformed_" + original_filename
    output_path = os.path.join(output_dir, output_filename)

    if hasattr(dataframe, "toPandas"):
        pandas_df = dataframe.toPandas()
    else:
        pandas_df = dataframe.copy()

    encrypted_df = modules.Security.encrypt_dataframe(pandas_df)
    encrypted_df.to_csv(output_path, index=False)

    print(f"Encrypted CSV saved to {output_path}")
    return output_path


def save_dataframe_to_mysql(dataframe, host, user, password, database, table_name):
    if hasattr(dataframe, "toPandas"):
        pandas_df = dataframe.toPandas()
    else:
        pandas_df = dataframe.copy()

    encrypted_df = modules.Security.encrypt_dataframe(pandas_df)

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
    for column_name in encrypted_df.columns:
        column_defs.append(f"`{column_name}` TEXT")

    create_table_sql = f"""
    CREATE TABLE {table_name} (
        {', '.join(column_defs)}
    )
    """
    cursor.execute(create_table_sql)

    columns_sql = ", ".join([f"`{col}`" for col in encrypted_df.columns])
    placeholders = ", ".join(["%s"] * len(encrypted_df.columns))
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"

    rows = [tuple(row) for row in encrypted_df.itertuples(index=False, name=None)]
    cursor.executemany(insert_sql, rows)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Encrypted data saved to MySQL table {database}.{table_name}")