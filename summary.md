# Distributed Systems & Concurrency — Unified, Bottom-Up Summary

> This document is a **single, self-contained synthesis** of the entire lecture sequence:
> asynchronous control flow → channels → actors → STM → MVU → RPC → replicated data → collective computation.
> It is written as a **conceptual stack**, from hardware constraints to large-scale distributed analytics.

---

## 0. The Fundamental Constraint

All models discussed exist because of one fact:

**Computation is fast; coordination is slow and failure-prone.**

Everything that follows is an attempt to:
- overlap waiting with useful work,
- restrict or structure nondeterminism,
- make failures survivable,
- and keep reasoning local.

---

## 1. Event Loops and Asynchronous Execution

### 1.1 Problem
A CPU must not block while waiting for I/O.  
If it blocks, it wastes time.

### 1.2 Event Loop
An event loop is a **scheduler** that repeatedly:
1. executes code until it cannot continue,
2. waits for external events (I/O, timers),
3. enqueues callbacks,
4. executes them one at a time.

Properties:
- single call stack,
- no preemption,
- no parallel execution of user code.

### 1.3 Consequence
Because the stack cannot be suspended arbitrarily, the *rest of the computation* must be stored explicitly.

That stored remainder is a **continuation**.

---

## 2. Continuations, CPS, Promises, async/await

### 2.1 Continuations
A continuation is:
> an explicit representation of “what happens next”.

Instead of:
```
x = f()
g(x)
```
we write:
```
f(k)   where k(x) = g(x)
```

### 2.2 CPS (Continuation-Passing Style)
- functions never return,
- they call a continuation instead,
- control flow becomes explicit.

This is not stylistic — it is *forced* by non-blocking runtimes.

### 2.3 Promises
Promises are **reified continuations**:
- a box for a future value,
- `.then` registers the continuation,
- errors propagate forward.

Promises form a **monad**:
```
return = Promise.resolve
bind   = then
```

### 2.4 async/await
`await` does **not block the thread**.
It:
- captures the continuation,
- returns control to the event loop,
- resumes when the promise settles.

This is CPS hidden behind syntax.

---

## 3. Channels and Communicating Sequential Processes (CSP)

### 3.1 CSP Model
- many sequential processes,
- no shared mutable state,
- explicit communication via channels.

### 3.2 Rendezvous Channels
- send and receive synchronize,
- neither side proceeds alone,
- creates a strong happens-before edge.

### 3.3 select / Guarded Commands
- wait on multiple communications,
- if several are ready, choose arbitrarily,
- explicit nondeterminism.

### 3.4 Properties
- races eliminated by construction,
- deadlocks still possible,
- coordination is explicit and local.

---

## 4. The Actor Model

### 4.1 Actor Definition
An actor has:
- a unique identity (PID),
- private local state,
- an unbounded mailbox,
- a behavior function.

On message receipt, an actor may:
- send messages,
- create actors,
- change its own behavior.

### 4.2 Semantics
- one message processed at a time,
- asynchronous send (never blocks),
- per-sender message ordering,
- no shared memory.

### 4.3 Continuations as Actors
A “reply-to” actor *is a continuation*.
Distributed CPS:
```
send(server, {request, reply_to})
```

### 4.4 Fault Model
- crash isolation,
- “let it crash” philosophy,
- supervision trees restart failed actors.

Deadlock becomes **protocol-level**, not primitive-level.

---

## 5. Software Transactional Memory (STM)

### 5.1 Motivation
Locks prevent interleavings.
STM allows interleavings but restricts **visibility**.

### 5.2 Transactions
A transaction:
- executes tentatively,
- commits atomically,
- or aborts with no effect.

### 5.3 Correctness
- **Serializability**: same effect as some serial order.
- **Opacity**: even aborted transactions see consistent state.

### 5.4 STM API (Haskell)
```
TVar a
readTVar  :: TVar a -> STM a
writeTVar :: TVar a -> a -> STM ()
atomically :: STM a -> IO a
retry
orElse
```

### 5.5 Properties
- no deadlocks,
- lock-free progress,
- starvation possible.

STM hides continuations and retries inside the runtime.

---

## 6. Model–View–Update (MVU)

### 6.1 Core Loop (Mealy Machine)
```
Model × Event → (Model, Action)
```

### 6.2 Structure
```
init    : Model
update  : Event -> Model -> (Model, Cmd Event)
view    : Model -> Html Event
```

### 6.3 Key Principles
- single global state,
- pure update function,
- effects are data,
- events drive all change.

### 6.4 Consequences
- no races,
- no deadlocks,
- deterministic state evolution,
- trivial testing.

MVU is effectively a **single-actor system** with a disciplined event loop.

---

## 7. Remote Procedure Calls (RPC)

### 7.1 Illusion
RPC pretends:
> remote calls behave like local calls.

This is false.

### 7.2 Failure Reality
- messages can be lost, duplicated, delayed,
- servers may crash mid-execution,
- timeouts are indistinguishable from slowness.

### 7.3 Semantics
- normal return ⇒ executed exactly once,
- error ⇒ executed zero or one times.

### 7.4 Tooling
- IDLs define data contracts,
- serialization enforces value semantics,
- retries, backoff, circuit breakers required.

RPC is **message passing + hidden continuations + failure**.

---

## 8. Replicated Data

### 8.1 Goal
Appear as a single coherent system despite:
- multiple copies,
- independent failures,
- unreliable networks.

### 8.2 State Machine Replication
Replicate a deterministic state machine.
All replicas apply the **same operations in the same order**.

### 8.3 Replication Schemes
- active replication,
- primary–backup,
- chain replication,
- quorum systems,
- consensus (Paxos/Raft).

### 8.4 CAP
Under partition:
- choose **consistency** or **availability**.

### 8.5 Logical Time
- Lamport clocks: total order, no concurrency detection.
- Vector clocks: exact causality, detect concurrency.

### 8.6 CRDTs
Design data so:
- order doesn’t matter,
- duplication doesn’t matter,
- merging is deterministic.

Based on **semilattices**:
- associative,
- commutative,
- idempotent.

Enable coordination-free, eventually consistent systems.

---

## 9. Collective Computation (Dryad, Spark)

### 9.1 Cost Model (BSP)
- computation cheap,
- communication expensive,
- minimize synchronization.

### 9.2 Dataflow DAGs
- vertices = computation,
- edges = data streams,
- explicit communication topology.

### 9.3 Spark RDDs
- immutable, partitioned datasets,
- transformations are lazy,
- actions trigger execution.

### 9.4 Partitioning
Data placement determines computation placement.

### 9.5 Shuffle
- wide dependency,
- all-to-all communication,
- dominant cost.

### 9.6 Fusion
Narrow dependencies are fused into stages.
Wide dependencies create stage boundaries.

### 9.7 Lineage
Fault tolerance via recomputation:
- record how data was derived,
- rebuild lost partitions deterministically.

---

## 10. Unifying Perspective

All models address **coordination under nondeterminism**:

| Layer | Abstraction | What it controls |
|------|-------------|------------------|
| Event loop | Scheduling | When code runs |
| Continuations | Control flow | What runs next |
| Promises | Futures | Asynchronous sequencing |
| Channels | Synchronization | When processes meet |
| Actors | Isolation | Who owns state |
| STM | Visibility | What becomes visible |
| MVU | Determinism | How state evolves |
| RPC | Distribution | Where code runs |
| Replication | Consistency | Which order matters |
| Spark | Dataflow | Where data moves |

---

## 11. Core Insight

> **As systems scale, correctness comes from restricting structure, not adding freedom.**

Each abstraction removes possibilities:
- callbacks → promises → MVU,
- shared memory → actors → CRDTs,
- ad-hoc threads → dataflow DAGs.

Understanding *where* an abstraction sits tells you:
- what failures it tolerates,
- what guarantees it provides,
- and what it deliberately forbids.



## 12 Klausur Infromationen

- sehr sicher Distributation, Parralel, Concurrency erklären und was jeweils dahinter liegt in eigenen Worten
- work span, task pfad --> kritischer pfad 
- alle von den Gesetzen in folien 0.pdf
- gather, scatter, scan kommen safe dran in spark reduce by key
- the matrix speicherungen ineiander übergehen lassen
- sortier algorthmen mit konzepten scan und so ... --> super schwere frgae mit segmented scan intuition
- bei asychn gab es quasi evolutionen (3 Stück wie die Logik aufbaut)
- asynch generators nicht macht es zu viel und zu schwer
- auch so dinge wie schleifen sollen asychron sein sonst gibt es einen freeze im interface
- grob das Problem von WaitGroups in Go
