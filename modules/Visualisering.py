import os
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import modules.Security


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

    decrypted_df = modules.Security.decrypt_dataframe(df)
    decrypted_df = modules.Security.cast_iris_columns(decrypted_df)

    return decrypted_df


def create_scatter_plot(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(df["sepal_length"], df["petal_length"])
    plt.title("Scatter Plot of Sepal Length vs Petal Length")
    plt.xlabel("Sepal Length")
    plt.ylabel("Petal Length")
    plt.savefig(os.path.join(output_dir, "scatter_plot.png"))
    plt.close()

    print(f"Scatter plot saved to {output_dir}/scatter_plot.png")


def create_histogram(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.hist(df["petal_width"], bins=10)
    plt.title("Histogram of Petal Width")
    plt.xlabel("Petal Width")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(output_dir, "histogram.png"))
    plt.close()

    print(f"Histogram saved to {output_dir}/histogram.png")


def create_boxplot(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

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

    fig.suptitle("Boxplots of Iris Measurements")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "boxplot.png"))
    plt.close()

    print(f"Boxplot saved to {output_dir}/boxplot.png")