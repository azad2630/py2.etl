import os
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import modules.Security


def load_dataframe_from_mysql(host, user, password, database, table_name):
    # Opretter forbindelse til MySQL-databasen
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Henter alle rækker fra den angivne tabel
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)

    # Lukker databaseforbindelsen efter data er læst
    connection.close()

    # Dekrypterer alle værdier i DataFrame
    decrypted_df = modules.Security.decrypt_dataframe(df)

    # Konverterer de numeriske iris-kolonner fra tekst til tal
    decrypted_df = modules.Security.cast_iris_columns(decrypted_df)

    # Returnerer den dekrypterede og konverterede DataFrame
    return decrypted_df


def create_scatter_plot(df, output_dir):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_dir, exist_ok=True)

    # Opretter en figur med angivet størrelse
    plt.figure(figsize=(8, 6))

    # Laver et scatter plot med sepal_length på x-aksen
    # og petal_length på y-aksen
    plt.scatter(df["sepal_length"], df["petal_length"])

    # Tilføjer titel og akse-navne
    plt.title("Scatter Plot of Sepal Length vs Petal Length")
    plt.xlabel("Sepal Length")
    plt.ylabel("Petal Length")

    # Gemmer figuren som PNG-fil i output-mappen
    plt.savefig(os.path.join(output_dir, "scatter_plot.png"))

    # Lukker figuren for at frigive hukommelse
    plt.close()

    # Udskriver hvor billedet blev gemt
    print(f"Scatter plot saved to {output_dir}/scatter_plot.png")


def create_histogram(df, output_dir):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_dir, exist_ok=True)

    # Opretter en figur med angivet størrelse
    plt.figure(figsize=(8, 6))

    # Laver et histogram over kolonnen petal_width med 10 bins
    plt.hist(df["petal_width"], bins=10)

    # Tilføjer titel og akse-navne
    plt.title("Histogram of Petal Width")
    plt.xlabel("Petal Width")
    plt.ylabel("Frequency")

    # Gemmer figuren som PNG-fil i output-mappen
    plt.savefig(os.path.join(output_dir, "histogram.png"))

    # Lukker figuren for at frigive hukommelse
    plt.close()

    # Udskriver hvor billedet blev gemt
    print(f"Histogram saved to {output_dir}/histogram.png")


def create_boxplot(df, output_dir):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_dir, exist_ok=True)

    # Opretter et 2x2 layout til fire boxplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Laver boxplot for sepal_length
    axes[0, 0].boxplot(df["sepal_length"])
    axes[0, 0].set_title("Sepal Length")
    axes[0, 0].set_ylabel("Value")

    # Laver boxplot for sepal_width
    axes[0, 1].boxplot(df["sepal_width"])
    axes[0, 1].set_title("Sepal Width")
    axes[0, 1].set_ylabel("Value")

    # Laver boxplot for petal_length
    axes[1, 0].boxplot(df["petal_length"])
    axes[1, 0].set_title("Petal Length")
    axes[1, 0].set_ylabel("Value")

    # Laver boxplot for petal_width
    axes[1, 1].boxplot(df["petal_width"])
    axes[1, 1].set_title("Petal Width")
    axes[1, 1].set_ylabel("Value")

    # Tilføjer samlet titel til hele figuren
    fig.suptitle("Boxplots of Iris Measurements")

    # Justerer layout så elementer ikke overlapper
    plt.tight_layout()

    # Gemmer figuren som PNG-fil i output-mappen
    plt.savefig(os.path.join(output_dir, "boxplot.png"))

    # Lukker figuren for at frigive hukommelse
    plt.close()

    # Udskriver hvor billedet blev gemt
    print(f"Boxplot saved to {output_dir}/boxplot.png")