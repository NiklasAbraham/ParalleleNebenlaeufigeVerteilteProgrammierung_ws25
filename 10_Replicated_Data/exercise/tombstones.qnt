module tombstones {


  type Element = int

  type State = Set[Element] // TODO


  var server1: State
  var server2: State


  action init = assert(false) // TODO


  action add1(x: Element): bool = assert(false) // TODO

  action add2(x: Element): bool = assert(false) // TODO

  action remove1(x: Element): bool = assert(false) // TODO

  action remove2(x: Element): bool = assert(false) // TODO

  def merge(s1: State, s2: State): State = Set() // TODO

  action synchronize1: bool = assert(false) // TODO

  action synchronize2: bool = assert(false) // TODO


  action step =
    any {
      add1(0),
      add2(0),
      add1(1),
      add2(1),
      remove1(0),
      remove2(0),
      remove1(1),
      remove2(1),
      synchronize1,
      synchronize2,
    }


  def view(state: State): Set[Element] = Set() // TODO


  val sameIfMerged =
    view(merge(server1, server2)) == view(merge(server2, server1))

  temporal eventualConsistency =
    eventually(view(server1) == view(server2))


  run example =
    init
      .then(add1(0))
      .then(add2(1))
      .then(remove1(0))
      .then(synchronize1)
      .then(synchronize2)
      .expect(view(server1) == view(server2))

}

