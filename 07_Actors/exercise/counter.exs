defmodule Counter do
  def start do
    Process.flag(:trap_exit, true)
    try do
      case Process.register(self(), :counter) do
        true ->
          IO.puts("Started as primary")
          primary(0)
        false ->
          wait_and_link()
          backup(0)
      end
    rescue
      ArgumentError ->
        wait_and_link()
        backup(0)
    end
  end

  def wait_and_link do
    case Process.whereis(:counter) do
      nil ->
        Process.sleep(10)
        wait_and_link()
      primary_pid ->
        Process.link(primary_pid)
        IO.puts("Started as backup, linked to primary")
    end
  end

  def primary(n) do
    receive do
      :increment ->
        primary(n + 1)
      :display ->
        IO.puts("Count: #{n}")
        primary(n)
    end
  end

  def backup(n) do
    receive do
      {:EXIT, _pid, _reason} ->
        Process.sleep(50)
        case Process.register(self(), :counter) do
          true ->
            IO.puts("Backup took over as primary")
            primary(n)
          false ->
            backup(n)
        end
      :increment ->
        backup(n + 1)
      :display ->
        IO.puts("Count: #{n}")
        backup(n)
    end
  end
end

# Start primary
primary_pid = spawn(fn -> Counter.start() end)

# Start backup
_backup_pid = spawn(fn -> Counter.start() end)

# Test the counter
Process.sleep(100)
send(:counter, :increment)
send(:counter, :increment)
send(:counter, :display)

# Simulate primary crash
Process.sleep(100)
Process.exit(primary_pid, :kill)

# Wait a bit for backup to take over
Process.sleep(300)

# Test that backup is now handling requests
counter_pid = Process.whereis(:counter)
if counter_pid != nil do
  send(:counter, :increment)
  send(:counter, :display)
end

Process.sleep(100)

