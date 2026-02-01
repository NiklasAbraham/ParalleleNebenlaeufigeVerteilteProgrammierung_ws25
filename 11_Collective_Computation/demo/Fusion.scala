import org.apache.spark.{SparkConf, SparkContext}

object Fusion {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext(new SparkConf().setAppName("Fusion").setMaster("local[*]"))

    val result = sc.parallelize(1 to 100, 4)
      .map {x => x * 2 }
      .filter { x => x > 50 }
      .map { x => (x, x + 1) }
      .groupByKey()
      .mapValues { x => x.sum }

    println(result.toDebugString)
    result.collect()

    println("Check http://localhost:4040")
    Thread.sleep(60000)

    sc.stop()
  }
}

