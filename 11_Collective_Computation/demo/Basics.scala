import org.apache.spark.SparkContext
import org.apache.spark.SparkConf

object Basics {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext( new SparkConf().setAppName("Basics").setMaster("local[*]"))

    val text = sc.textFile("pride_and_prejudice.txt")
    val words = text.map(line => line.split("\\s+").length)
    val total = words.reduce(_ + _)

    println(total)

    sc.stop()
  }
}
