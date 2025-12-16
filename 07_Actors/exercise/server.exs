
defmodule Server do
  def start do
    Process.register(self(), :server)
    {:ok, listen_socket} = :gen_tcp.listen(8080, [active: false, reuseaddr: true])
    spawn(fn -> accept_loop(listen_socket) end)
    Process.sleep(:infinity)
  end

  def accept_loop(listen_socket) do
    {:ok, client_socket} = :gen_tcp.accept(listen_socket)
    spawn(fn -> handle_client(client_socket) end)
    accept_loop(listen_socket)
  end

  def handle_client(client_socket) do
    engine_pid = wait_for_engine()
    if engine_pid != nil do
      spawn(fn -> client_to_engine_loop(client_socket, engine_pid) end)
      engine_to_client_loop(client_socket, engine_pid)
    else
      :gen_tcp.close(client_socket)
    end
  end

  def wait_for_engine do
    case Process.whereis(:engine) do
      nil ->
        Process.sleep(100)
        wait_for_engine()
      pid ->
        pid
    end
  end

  def client_to_engine_loop(client_socket, engine_pid) do
    case :gen_tcp.recv(client_socket, 0) do
      {:ok, _data} ->
        send(engine_pid, {:message, self()})
        receive do
          {:reply, reply} ->
            :gen_tcp.send(client_socket, reply <> "\n")
            client_to_engine_loop(client_socket, engine_pid)
        end
      {:error, :closed} ->
        :ok
      {:error, _} ->
        :ok
    end
  end

  def engine_to_client_loop(_client_socket, _engine_pid) do
    receive do
      _ -> :ok
    end
  end
end

