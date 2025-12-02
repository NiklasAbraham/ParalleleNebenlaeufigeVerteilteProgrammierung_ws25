package main

import "fmt"

func generate(n int, channel chan<- int) {
	for i := 2; i <= n; i++ {
		channel <- i
	}
	close(channel)
}

func filter(prime int, input <-chan int, output chan<- int) {
	for num := range input {
		if num%prime != 0 {
			output <- num
		}
	}
	close(output)
}

func main() {
	n := 100

	ch := make(chan int)
	go generate(n, ch)

	for {
		prime, ok := <-ch
		if !ok {
			break
		}
		fmt.Println(prime)
		nextCh := make(chan int)
		go filter(prime, ch, nextCh)
		ch = nextCh
	}
}
