from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def transform_iris_setosa(input_file):
    # Opretter en SparkSession som bruges til at arbejde med PySpark
    spark = SparkSession.builder \
        .appName("IrisTransform") \
        .getOrCreate()

    # Læser CSV-filen ind som Spark DataFrame
    # header=False betyder at filen læses uden kolonnenavne i første række
    # inferSchema=True gør at Spark forsøger at finde de rigtige datatyper automatisk
    df = spark.read.csv(input_file, header=False, inferSchema=True)

    # Tildeler kolonnenavne til DataFrame
    df = df.toDF(
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species"
    )

    # Filtrerer DataFrame så kun rækker med arten Iris-setosa beholdes
    iris_setosa_df = df.filter(col("species") == "Iris-setosa")

    # Returnerer den transformerede DataFrame
    return iris_setosa_df