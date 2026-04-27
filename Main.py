import modules.Extract
import modules.Transform
import modules.Load
import modules.Visualisering


# URL til iris-datasættet som skal downloades
IRIS_download_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"

# Mappe til det originale downloadede input-data
input_folder = "input_data"

# Mappe til det transformerede og krypterede output-data
output_folder = "output_data"

# Mappe til gemte visualiseringer
visual_output = "visual_output"


def main():
    # Downloader inputfilen fra URL'en og gemmer den i input_folder
    input_file = modules.Extract.download_file_requests(
        IRIS_download_URL,
        output_folder=input_folder
    )

    # Transformerer inputdata med PySpark så kun Iris-setosa rækker beholdes
    iris_setosa_df = modules.Transform.transform_iris_setosa(input_file)

    # Gemmer det transformerede data som krypteret CSV-fil i output_folder
    modules.Load.save_dataframe_to_csv(
        iris_setosa_df,
        output_dir=output_folder,
        source_file_path=input_file
    )

    # Gemmer det transformerede data som krypteret tabel i MySQL
    modules.Load.save_dataframe_to_mysql(
        iris_setosa_df,
        host="localhost",
        user="etl_user",
        password="etl1234",
        database="iris_db",
        table_name="iris_setosa"
    )

    # Henter data tilbage fra MySQL, dekrypterer det og gør det klar til visualisering
    df = modules.Visualisering.load_dataframe_from_mysql(
        host="localhost",
        user="etl_user",
        password="etl1234",
        database="iris_db",
        table_name="iris_setosa"
    )

    # Laver og gemmer scatter plot
    modules.Visualisering.create_scatter_plot(df, visual_output)

    # Laver og gemmer histogram
    modules.Visualisering.create_histogram(df, visual_output)

    # Laver og gemmer boxplot
    modules.Visualisering.create_boxplot(df, visual_output)


# Sørger for at main() kun køres når filen startes direkte
if __name__ == "__main__":
    main()