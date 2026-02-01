import org.apache.spark.{SparkConf, SparkContext}

object LogisticRegression {
  def sigmoid(z: Double): Double = 1.0 / (1.0 + math.exp(-z))

  def main(args: Array[String]) = {
    val sc = new SparkContext(new SparkConf().setAppName("LogisticRegression").setMaster("local[*]"))

    val data = sc.parallelize(List(
      ((1.0, 2.0), 0.0),
      ((2.0, 1.0), 0.0),
      ((2.0, 3.0), 0.0),
      ((3.0, 2.0), 0.0),
      ((5.0, 6.0), 1.0),
      ((6.0, 5.0), 1.0),
      ((6.0, 7.0), 1.0),
      ((7.0, 6.0), 1.0),
    )).cache()

    var weight0 = 0.0
    var weight1 = 0.0
    var bias = 0.0

    for (i <- 1 to 30) {
      val gradients = data.map {
        case ((x0, x1), y) =>
          val prediction = sigmoid(bias + weight0 * x0 + weight1 * x1)
          val error = prediction - y
          (error, error * x0, error * x1)
      }
      val (bias_gradient, weight0_gradient, weight1_gradient) = gradients.reduce {
        case ((b1, w01, w11), (b2, w02, w12)) =>
          (b1 + b2, w01 + w02, w11 + w12)
      }
      bias = bias - 0.1 * bias_gradient
      weight0 = weight0 - 0.1 * weight0_gradient
      weight1 = weight1 - 0.1 * weight1_gradient
    }

    println(s"weight0 = $weight0, weight1 = $weight1, bias = $bias")

    val correct = data.map {
      case ((x0, x1), y) =>
        val prediction = sigmoid(bias + weight0 * x0 + weight1 * x1)
        if ((prediction >= 0.5 && y == 1.0) || (prediction < 0.5 && y == 0.0)) 1 else 0
    }.reduce(_ + _)

    val accuracy = correct.toDouble / data.count()
    println(s"Accuracy: ${accuracy * 100}%")

    sc.stop()
  }
}
