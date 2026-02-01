import org.apache.spark.SparkContext
import org.apache.spark.SparkConf

object MapReduce {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext(new SparkConf().setAppName("MapReduce").setMaster("local[*]"))

    val text = sc.textFile("pride_and_prejudice.txt")
    val words = text.flatMap(line => line.split("\\s+"))
    val pairs = words.map(word => (word, 1))
    val counts = pairs.reduceByKey(_ + _)

    counts.take(10).foreach(println)

    sc.stop()
  }
}

