package main

import (
	"fmt"
)

func main() {
	queue1 := make(chan int, 2)
	queue2 := make(chan int, 2)

	close(queue1)
	queue1 <- 123

	go producer(queue1)
	go transformer(queue1, queue2)
	consumer(queue2)
}

func producer(queue1 chan int) {
	for i := 0; i < 5; i++ {
		queue1 <- i
	}
	close(queue1)
}

func transformer(queue1, queue2 chan int) {
	for {
		value, ok := <-queue1
		if (!ok) {
                close(queue2);
		return;
		}
		queue2 <- value + 1
	}
}

func consumer(queue2 chan int) {
	for value := range queue2 {
		fmt.Println(value)
	}
}
