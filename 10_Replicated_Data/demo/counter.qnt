module counter {

  pure def max(x: int, y: int): int =
    if (x < y) { y } else { x }

  type Operation =
    | Increment
    | Decrement

  type State = { value1: int, value2: int }

  var server1: State
  var server2: State
  var todo: List[Operation]

  action init = all {
    server1' = { value1: 0, value2: 0 },
    server2' = { value1: 0, value2: 0 },
    todo' = [Decrement],
  }

  action update1: bool = all {
    todo.length() > 0,
    server1' = {
      match todo.head() {
        | Increment => { value1: server1.value1 + 1, value2: server1.value2 }
        | Decrement => { value1: server1.value1 - 1, value2: server1.value2 }
      }
    },
    todo' = todo.tail(),
    server2' = server2,
  }

  action update2: bool = all {
    todo.length() > 0,
    server2' = {
      match todo.head() {
        | Increment => { value1: server2.value1, value2: server2.value2 + 1 }
        | Decrement => { value1: server2.value1, value2: server2.value2 - 1 }
      }
    },
    todo' = todo.tail(),
    server1' = server1,
  }

  def merge(state1: State, state2: State): State =
    { value1: max(state1.value1, state2.value1), value2: max(state1.value2, state2.value2) }

  action synchronize1: bool = all {
    server1' = merge(server1, server2),
    server2' = server2,
    todo' = todo,
  }

  action synchronize2: bool = all {
    server2' = merge(server2, server1),
    server1' = server1,
    todo' = todo,
  }

  action step() =
    any {
      update1,
      update2,
      synchronize1,
      synchronize2,
    }

  def view(state: State): int = state.value1 + state.value2

  run example = init.then(update1).then(update2).then(synchronize1).then(synchronize2).expect(view(server1) == view(server2))

  val sameIfSynchronized = view(merge(server1, server2)) == view(merge(server2, server1))

  temporal eventualConsistency =
    eventually(view(server1) == view(server2))

}