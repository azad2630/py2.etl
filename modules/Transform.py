from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def transform_iris_setosa(input_file):
    spark = SparkSession.builder \
        .appName("IrisTransform") \
        .getOrCreate()

    df = spark.read.csv(input_file, header=False, inferSchema=True)

    df = df.toDF(
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species"
    )

    iris_setosa_df = df.filter(col("species") == "Iris-setosa")

    return iris_setosa_df