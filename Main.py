import modules.Extract
import modules.Transform
import modules.Load
import modules.Visualisering


IRIS_download_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
input_folder = "input_data"
output_folder = "output_data"


def main():
    input_file = modules.Extract.download_file_requests(IRIS_download_URL, output_folder=input_folder)

    iris_setosa_df = modules.Transform.transform_iris_setosa(input_file)

    modules.Load.save_dataframe_to_csv(
        iris_setosa_df,
        output_dir=output_folder,
        source_file_path=input_file
    )

    modules.Load.save_dataframe_to_mysql(
    iris_setosa_df,
    host="localhost",
    user="etl_user",
    password="etl1234",
    database="iris_db",
    table_name="iris_setosa"
    )

    df = modules.Visualisering.load_dataframe_from_mysql(
    host="localhost",
    user="etl_user",
    password="etl1234",
    database="iris_db",
    table_name="iris_setosa"
    )

    modules.Visualisering.create_scatter_plot(df, "visual_output")
    modules.Visualisering.create_histogram(df, "visual_output")
    modules.Visualisering.create_boxplot(df, "visual_output")


if __name__ == "__main__":
    main()