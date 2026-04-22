from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def transform_iris_setosa(input_file):
    spark = SparkSession.builder \
        .appName("IrisTransform") \
        .getOrCreate()
    
    # spark.sparkContext.setLogLevel("ERROR")

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


# def run_transform_test(input_file):
#     spark, iris_setosa_df = transform_iris_setosa(input_file)

#     iris_setosa_df.show()

#     print("Antal rækker:")
#     print(iris_setosa_df.count())

#     spark.stop()


# if __name__ == "__main__":
#     run_transform_test("input_data/iris.csv")