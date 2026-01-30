# Exercise 10: Replicated Data

## Replication Scheme

Implement any replication schemes either from the lecture or your own using any
language or technology of your choice. There should be a single replicated
integer value and it should be possible for multiple clients to interact with
the service by putting a new number and getting the current one. Document which
levels of fault tolerance and consistency you provide.

Optional Challenge: use a tool like `ab` to measure the read and write latency
of your service.

## Two-Phase Sets

Model Two-Phase Sets in Quint where two servers update a shared set of numbers.
Both should be able to add and remove elements, and to sychronize with each
other by merging their states. Define the type of each server's state, a
merge function, a view function, and update actions.

Use file `tombstones.qnt` as a starting point.

In the end, try to check that eventual consistency holds:

```
quint verify tombstones.qnt --max-steps=5 --temporal=eventualConsistency
```

## Collaborative Editing

Build a collaborative application using either Yjs https://yjs.dev/ or Automerge
https://automerge.org/. It should support multiple users, either peer-to-peer
with YJs and `y-webrtc`, or using the public Automerge sync server
`sync.automerge.org`, or by building your own server following online tutorials.
Some ideas for what to edit are a shared todo list, text editor, or drawing
canvas.

