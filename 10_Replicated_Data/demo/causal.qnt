module causal {

  pure def max(x: int, y: int): int =
    if (x < y) { y } else { x }

  type Message = { sender: str, clock: str -> int, value: int }
  type Server = { state: int, seen: str -> int }

  pure val network = Set(
    { sender: "c1", clock: Map("c1" -> 1, "c2" -> 0), value: 1 },
    { sender: "c1", clock: Map("c1" -> 2, "c2" -> 0), value: 2 },
    { sender: "c2", clock: Map("c1" -> 0, "c2" -> 1), value: 3 },
    { sender: "c2", clock: Map("c1" -> 2, "c2" -> 2), value: 4 }
  )

  var server1: Server
  var server2: Server

  action init = all {
    server1' = { state: 0, seen: Map("c1" -> 0, "c2" -> 0) },
    server2' = { state: 0, seen: Map("c1" -> 0, "c2" -> 0) },
  }

  action receive1(message: Message): bool = all {
    message.clock.get(message.sender) == server1.seen.get(message.sender) + 1,
    message.sender != "c1" implies message.clock.get("c1") <= server1.seen.get("c1"),
    message.sender != "c2" implies message.clock.get("c2") <= server1.seen.get("c2"),
    server1' = {
      state: message.value,
      seen: server1.seen.set(message.sender, message.clock.get(message.sender)),
    },
    server2' = server2,
  }

  action receive2(message: Message): bool = all {
    message.clock.get(message.sender) == server2.seen.get(message.sender) + 1,
    message.sender != "c1" implies message.clock.get("c1") <= server2.seen.get("c1"),
    message.sender != "c2" implies message.clock.get("c2") <= server2.seen.get("c2"),
    server2' = {
      state: message.value,
      seen: server2.seen.set(message.sender, message.clock.get(message.sender)),
    },
    server1' = server1,
  }

  action step =
    nondet message = oneOf(network)
    any {
      receive1(message),
      receive2(message),
    }

  val sameState = server1.state == server2.state

  val sameStateAfterSeen =
    server1.seen == server2.seen implies
    server1.state == server2.state

  pure def beforeClock(clock1: str -> int, clock2: str -> int): bool =
    clock1.get("c1") <= clock2.get("c1") and
    clock1.get("c2") <= clock2.get("c2")

  val latestStateSeen = any {
    server1.state == 0,
    network.exists(m1 =>
      m1.clock.get(m1.sender) <= server1.seen.get(m1.sender) and
      server1.state == m1.value and
      network.forall(m2 =>
        m2.clock.get(m2.sender) <= server1.seen.get(m2.sender) implies
        (m1.clock == m2.clock or not(beforeClock(m1.clock, m2.clock)))
      )
    )
  }

  val eventuallyFour =
    (server1.seen == Map("c1" -> 2, "c2" -> 2)) implies
    server1.state == 4

}