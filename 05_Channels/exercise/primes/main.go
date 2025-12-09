package main

import (
	"fmt"
	"time"
)

func generate(n int, channel chan<- int) {
	for i := 2; i <= n; i++ {
		channel <- i
	}
	close(channel)
}

func filter(prime int, input <-chan int, output chan<- int) {
	for n := range input {
		if n%prime != 0 {
			output <- n
		}
	}
	close(output)
}

func main() {
	n := 1000000

	start := time.Now()

	input := make(chan int)
	go generate(n, input)

	for {
		prime, ok := <-input
		if !ok {
			break 
		}

		fmt.Println(prime)

		next := make(chan int)
		go filter(prime, input, next)
		input = next 
	}

	fmt.Printf("Sieved up to %d in %s\n", n, time.Since(start))
}
