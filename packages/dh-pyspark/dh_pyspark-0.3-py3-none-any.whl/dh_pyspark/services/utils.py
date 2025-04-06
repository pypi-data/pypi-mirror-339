from pyspark.sql import SparkSession


def log_spark_job(spark: SparkSession, description: str):
    """
    Helper function to log and set Spark job descriptions with detailed information.
    """

    # Set the job description for the Spark UI
    spark.sparkContext.setJobDescription(description)

    # Log the message to the console
    print(f"--------------------------------------------------"
          f"\n{description}"
          f"\n--------------------------------------------------")