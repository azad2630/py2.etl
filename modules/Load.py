import os
import pandas as pd
import mysql.connector
import modules.Security


def save_dataframe_to_csv(dataframe, output_dir, source_file_path):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_dir, exist_ok=True)

    # Henter originalt filnavn fra source_file_path
    original_filename = os.path.basename(source_file_path)

    # Laver nyt filnavn ved at tilføje "transformed_" foran originalt navn
    output_filename = "transformed_" + original_filename

    # Samler fuld sti til outputfilen
    output_path = os.path.join(output_dir, output_filename)

    # Hvis input er en Spark DataFrame, konverteres den til Pandas DataFrame
    if hasattr(dataframe, "toPandas"):
        pandas_df = dataframe.toPandas()
    else:
        # Hvis input allerede er en Pandas DataFrame, laves en kopi
        pandas_df = dataframe.copy()

    # Krypterer hele DataFrame med modulet Security
    encrypted_df = modules.Security.encrypt_dataframe(pandas_df)

    # Gemmer den krypterede DataFrame som CSV-fil
    # index=False betyder at rækkeindeks ikke gemmes i filen
    encrypted_df.to_csv(output_path, index=False)

    # Udskriver hvor den krypterede CSV blev gemt
    print(f"Encrypted CSV saved to {output_path}")

    # Returnerer stien til den gemte CSV-fil
    return output_path


def save_dataframe_to_mysql(dataframe, host, user, password, database, table_name):
    # Hvis input er en Spark DataFrame, konverteres den til Pandas DataFrame
    if hasattr(dataframe, "toPandas"):
        pandas_df = dataframe.toPandas()
    else:
        # Hvis input allerede er en Pandas DataFrame, laves en kopi
        pandas_df = dataframe.copy()

    # Krypterer hele DataFrame før data gemmes i databasen
    encrypted_df = modules.Security.encrypt_dataframe(pandas_df)

    # Opretter forbindelse til MySQL-server uden at vælge database endnu
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    # Opretter databasen hvis den ikke allerede findes
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

    # Lukker første forbindelse
    cursor.close()
    connection.close()

    # Opretter ny forbindelse, nu direkte til den ønskede database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    # Sletter tabellen hvis den allerede findes
    # Det sikrer at gamle data overskrives ved hver kørsel
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Bygger kolonnedefinitioner til SQL-tabellen
    # Alle kolonner sættes til TEXT, fordi krypterede værdier gemmes som tekst
    column_defs = []
    for column_name in encrypted_df.columns:
        column_defs.append(f"`{column_name}` TEXT")

    # Laver SQL-kommando til at oprette tabellen
    create_table_sql = f"""
    CREATE TABLE {table_name} (
        {', '.join(column_defs)}
    )
    """
    cursor.execute(create_table_sql)

    # Laver kommando til INSERT af alle kolonner
    columns_sql = ", ".join([f"`{col}`" for col in encrypted_df.columns])
    placeholders = ", ".join(["%s"] * len(encrypted_df.columns))
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"

    # Omdanner DataFrame-rækker til tuples så de kan indsættes i MySQL
    rows = [tuple(row) for row in encrypted_df.itertuples(index=False, name=None)]

    # Indsætter alle rækker i tabellen
    cursor.executemany(insert_sql, rows)

    # Gemmer ændringer i databasen
    connection.commit()

    # Lukker forbindelse og cursor
    cursor.close()
    connection.close()

    # Udskriver at data er gemt i databasen
    print(f"Encrypted data saved to MySQL table {database}.{table_name}")