package main

func main() {
	channel := make(chan int)
	value := <-channel
	channel <- value
}

