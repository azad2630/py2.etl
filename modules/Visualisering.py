import os
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector


def load_dataframe_from_mysql(host, user, password, database, table_name):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)

    connection.close()
    return df


def create_scatter_plot(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(df["sepal_length"], df["petal_length"])
    plt.title("Scatter Plot: Sepal Length vs Petal Length")
    plt.xlabel("Sepal Length")
    plt.ylabel("Petal Length")
    plt.savefig(os.path.join(output_folder, "scatter_plot.png"))
    plt.close()

    print(f"Scatter plot saved to {output_folder}/scatter_plot.png")


def create_histogram(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.hist(df["petal_width"], bins=10)
    plt.title("Histogram: Petal Width")
    plt.xlabel("Petal Width")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(output_folder, "histogram.png"))
    plt.close()

    print(f"Histogram saved to {output_folder}/histogram.png")


def create_boxplot(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    axes[0, 0].boxplot(df["sepal_length"])
    axes[0, 0].set_title("Sepal Length")
    axes[0, 0].set_ylabel("Value")

    axes[0, 1].boxplot(df["sepal_width"])
    axes[0, 1].set_title("Sepal Width")
    axes[0, 1].set_ylabel("Value")

    axes[1, 0].boxplot(df["petal_length"])
    axes[1, 0].set_title("Petal Length")
    axes[1, 0].set_ylabel("Value")

    axes[1, 1].boxplot(df["petal_width"])
    axes[1, 1].set_title("Petal Width")
    axes[1, 1].set_ylabel("Value")

    fig.suptitle("Boxplots: Iris Measurements")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "boxplot.png"))
    plt.close()

    print(f"Boxplot saved to {output_folder}/boxplot.png")


# if __name__ == "__main__":
#     output_folder = "visual_output"

#     df = load_dataframe_from_mysql(
#         host="localhost",
#         user="etl_user",
#         password="etl1234",
#         database="iris_db",
#         table_name="iris_setosa"
#     )

#     create_scatter_plot(df, output_folder)
#     create_histogram(df, output_folder)
#     create_boxplot(df, output_folder)