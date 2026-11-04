from pyspark.sql import SparkSession


def test_spark_session_starts():
    spark=(SparkSession.builder
            .master("local[2]")
            .appName("smoke-test")
            .getOrCreate()
            )

    df=spark.createDataFrame([(1,"a"),(2,"b")],["id","value"])
    assert df.count()==2
    spark.stop()
