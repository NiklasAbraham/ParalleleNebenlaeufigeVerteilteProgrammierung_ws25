# Exercise 11: Collective Computation

## Logistic Regression

Implement distributed logistic regression for two-dimensional points.

https://en.wikipedia.org/wiki/Logistic_regression

The classification algorithm takes weights `weight0`, `weight1` and bias `bias`
and classifies inputs `x0`, `x1` as belonging to class 0 when
`sigmoid(bias + weight0 * x0 + weight1 * x1) < 0.5` or to class 1 otherwise.
Your job is to find weights and bias `weight0`, `weight1`, `bias` that
minimize loss given pairs of points and labels using gradient descent.
For each data point `(x0, x1)` and label `y` compute the individual gradient:

```
val prediction = sigmoid(bias + weight0 * x0 + weight1 * x1)
val error = prediction - y
(error, error * x0, error * x1)
```

Then update the weights and bias with the sum of their gradients scaled by
`0.1`.

Use file `LogisticRegression.scala` as a starting point and run it with
`sbt run`.

Run the training algorithm for a fixed number of iterations and output the
accuracy, which is the ratio of points correctly classified, at the end.

Optional challenge: load the data points and labels from a file.

