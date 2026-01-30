module basics {

var x: int

action init = {
  x' = 0
}

action increment =
  x' = x + 1

action decrement =
  x' = x - 1

action step = any {
  increment,
  decrement,
}


val non_negative = x >= 0

temporal above_two = eventually(x > 2)

temporal again_zero = always(eventually(x == 0))

}