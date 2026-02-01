import org.apache.spark.{SparkConf, SparkContext}

object PageRank {
  def main(args: Array[String]) = {
    val sc = new SparkContext(new SparkConf().setAppName("PageRank").setMaster("local[*]"))

    val pages = sc.parallelize(List(
      "A" -> List(),
      "B" -> List("C"),
      "C" -> List("B"),
      "D" -> List("A", "B"),
      "E" -> List("B", "D", "F"),
      "F" -> List("B", "E"),
      "G" -> List("B", "E"),
      "H" -> List("B", "E"),
      "I" -> List("B", "E"),
      "J" -> List("E"),
      "K" -> List("E"),
    )).cache()

    var ranks = pages.mapValues(_ => 1.0)

    for (i <- 1 to 10) {
      val contributions = pages.join(ranks).flatMap {
        case (page, (links, rank)) =>
          links.map(link => (link, rank / links.size))
      }
      val jumps = pages.mapValues(_ => 0.15)
      val clicks = contributions.mapValues(0.85 * _)
      ranks = jumps.union(clicks).reduceByKey(_ + _)
    }

    ranks.collect().foreach(println)

    sc.stop()
  }
}
