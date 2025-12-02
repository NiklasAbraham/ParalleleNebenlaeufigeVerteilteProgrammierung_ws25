package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {

	listener, _ := net.Listen("tcp", ":8080")
	connection, _ := listener.Accept()
	writer := bufio.NewWriter(connection)

	input := make(chan string, 1)
	network := make(chan string, 1)

	go func() {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			input <- scanner.Text()
		}
	}()

	go func() {
		scanner := bufio.NewScanner(connection)
		for scanner.Scan() {
			network <- scanner.Text()
		}
	}()

	for {
		select {
		case message := <-input:
			writer.WriteString(message + "\n")
			writer.Flush()
		case message := <-network:
			fmt.Println(">", message)
		}
	}
}
