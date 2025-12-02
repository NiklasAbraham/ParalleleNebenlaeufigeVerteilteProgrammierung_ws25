package main

import "bufio"
import "net"
import "sync"

func main() {

	listener, _ := net.Listen("tcp", ":8080")

	clients := []net.Conn{}
	newclients := []net.Conn{}
	broadcast := make(chan string, 5)
	var mx sync.Mutex

	go func() {
		for {
			connection, _ := listener.Accept()
			scanner := bufio.NewScanner(connection)
			mx.Lock()
			newclients = append(newclients, connection)
			mx.Unlock()

			go func() {
				for scanner.Scan() {
					broadcast <- scanner.Text()
				}
			}()
		}
	}()

	for message := range broadcast {
		mx.Lock()
		for _, client := range clients {
			writer := bufio.NewWriter(client)
			writer.WriteString(message + "\n")
			writer.Flush()
		}
		mx.Unlock()
	}
}
