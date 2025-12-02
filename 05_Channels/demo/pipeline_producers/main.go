package main

import (
	"fmt"
	"sync"
	"runtime"
)

func main() {
	queue1 := make(chan int, 2)
	queue2 := make(chan int, 2)

	var wg sync.WaitGroup

	wg.Go(func() {
		producer(queue1)
	})

	wg.Add(1)
	go func() {
		producer(queue1)
		wg.Done()
	}()

	go transformer(queue1, queue2)

	go consumer(queue2)

	wg.Wait()
        close(queue1)
}

func producer(queue1 chan int) {
	for i := 0; i < 5; i++ {
		runtime.Gosched()
		queue1 <- i
	}
}

func transformer(queue1, queue2 chan int) {
	for value := range queue1 {
		queue2 <- value + 1
	}
	close(queue2)
}

func consumer(queue2 chan int) {
	for value := range queue2 {
		fmt.Println(value)
	}
}
