import org.apache.spark.{SparkConf, SparkContext}

object Grouping {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext(new SparkConf().setAppName("Grouping").setMaster("local[*]"))

    val pairs = sc.parallelize(List(("a", 1), ("b", 2), ("a", 3), ("b", 4), ("a", 5), ("b", 6)), 2)

    println("Running groupByKey")
    val grouped = pairs.groupByKey()
    grouped.mapValues(_.sum).collect().foreach(println)

    println("Running reduceByKey")
    val reduced = pairs.reduceByKey(_ + _)
    reduced.collect().foreach(println)

    sc.stop()
  }
}
