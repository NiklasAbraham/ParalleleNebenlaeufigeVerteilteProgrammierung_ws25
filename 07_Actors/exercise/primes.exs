defmodule Primes do

  def generate(n, pid) do
    for i <- 2..n do
      send(pid, {:number, i})
    end
    send(pid, :done)
  end

  def sieve() do
    receive do
      {:number, prime} ->
        IO.puts(prime)
        next = spawn(fn -> Primes.filter_loop(prime, nil) end)
        sieve_loop(next)
      :done ->
        :ok
    end
  end

  def sieve_loop(next) do
    receive do
      {:number, n} ->
        send(next, {:number, n})
        sieve_loop(next)
      :done ->
        send(next, :done)
        :ok
    end
  end

  def filter_loop(prime, next) do
    receive do
      {:number, n} ->
        if rem(n, prime) != 0 do
          if next == nil do
            IO.puts(n)
            new_next = spawn(fn -> Primes.filter_loop(n, nil) end)
            filter_loop(prime, new_next)
          else
            send(next, {:number, n})
            filter_loop(prime, next)
          end
        else
          filter_loop(prime, next)
        end
      :done ->
        if next != nil do
          send(next, :done)
        end
        :ok
    end
  end
end

n = 1000000
start = System.monotonic_time(:millisecond)
first = spawn(fn -> Primes.sieve() end)
Primes.generate(n, first)
Process.sleep(5000)
elapsed = System.monotonic_time(:millisecond) - start
IO.puts("Sieved up to #{n} in #{elapsed} ms")

