
defmodule Client do
  def start do
    {:ok, socket} = :gen_tcp.connect(String.to_charlist("localhost"), 8080, [:binary, active: false])
    main = self()
    spawn(fn -> stdin_loop(main) end)
    spawn(fn -> network_loop(socket, main) end)
    loop(socket)
  end

  def stdin_loop(main) do
    case IO.gets("") do
      :eof ->
        :ok
      data ->
        send(main, {:stdin, data})
        stdin_loop(main)
    end
  end

  def network_loop(socket, main) do
    case :gen_tcp.recv(socket, 0) do
      {:ok, data} ->
        send(main, {:network, data})
        network_loop(socket, main)
      {:error, :closed} ->
        :ok
      {:error, _} ->
        :ok
    end
  end

  def loop(socket) do
    receive do
      {:stdin, line} ->
        :gen_tcp.send(socket, line)
        loop(socket)
      {:network, data} ->
        IO.write("> #{data}")
        loop(socket)
    end
  end
end

