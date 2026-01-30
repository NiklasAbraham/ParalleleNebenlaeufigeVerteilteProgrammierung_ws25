module network {

  type Message = { sender: str, sequence: int, value: int }
  type Server = { state: int, seen: str -> int }

  pure val network = Set(
    { sender: "c1", sequence: 0, value: 1 },
    { sender: "c1", sequence: 1, value: 2 },
    { sender: "c2", sequence: 0, value: 3 },
    { sender: "c2", sequence: 1, value: 4 }
  )

  var server1: Server
  var server2: Server

  action init = all {
    server1' = { state: 0, seen: Map("c1" -> 0, "c2" -> 0) },
    server2' = { state: 0, seen: Map("c1" -> 0, "c2" -> 0) },
  }

  action receive1(message: Message): bool = all {
    server1.seen.get(message.sender) == message.sequence,
    server1' = {
      state: message.value,
      seen: server1.seen.set(message.sender, message.sequence + 1)
    },
    server2' = server2,
  }

  action receive2(message: Message): bool = all {
    server2.seen.get(message.sender) == message.sequence,
    server2' = {
      state: message.value,
      seen: server2.seen.set(message.sender, message.sequence + 1)
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

  val latestStateSeen = any {
    server1.state == 0,
    network.exists(m1 =>
      m1.sequence < server1.seen.get(m1.sender) and
      server1.state == m1.value and
      network.forall(m2 =>
        (m1.sender == m2.sender and m2.sequence < server1.seen.get(m2.sender)) implies
          m2.sequence <= m1.sequence
      )
    )
  }

}

