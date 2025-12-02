package main

import (
	"bufio"
	"io"
	"net"
)

func handleClient(clientConn net.Conn) {
	defer clientConn.Close()

	engineConn, err := net.Dial("tcp", ":9000")
	if err != nil {
		return
	}
	defer engineConn.Close()

	clientReader := bufio.NewReader(clientConn)
	clientWriter := bufio.NewWriter(clientConn)
	engineReader := bufio.NewReader(engineConn)
	engineWriter := bufio.NewWriter(engineConn)

	go func() {
		for {
			line, err := clientReader.ReadString('\n')
			if err != nil {
				if err != io.EOF {
					// Error reading from client
				}
				return
			}
			engineWriter.WriteString(line)
			engineWriter.Flush()
		}
	}()

	for {
		line, err := engineReader.ReadString('\n')
		if err != nil {
			if err != io.EOF {
				// Error reading from engine
			}
			return
		}
		clientWriter.WriteString(line)
		clientWriter.Flush()
	}
}

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	for {
		clientConn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleClient(clientConn)
	}
}

