import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object Laziness {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext(new SparkConf().setAppName("Laziness").setMaster("local[*]"))

    val values = sc.parallelize(1 to 20)

    println("Map:")
    val doubled = values.map { x => println(s"mapping: $x"); x * 2 }

    println("Filter:")
    val filtered = doubled.filter { x => println(s"filtering: $x"); x > 20 }

    println("Collect:")
    filtered.collect()

    sc.stop()
  }
}
