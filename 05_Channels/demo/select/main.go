package main

import (
	"fmt"
	"time"
)

func main() {
	input := make(chan string, 1)
	timeout := make(chan bool, 1)

	go func() {
		var text string
		fmt.Scanln(&text)
		input <- text
	}()

	go func() {
		time.Sleep(2 * time.Second)
		timeout <- true
	}()

	select {
	case text := <-input:
		fmt.Println("You entered:", text)
	case <-timeout:
		fmt.Println("Timeout!")
	}
}
