package main

import "fmt"
import "time"
import "runtime"

func main() {
	channel := make(chan int)

	go func() { fmt.Println("a"); channel <- 1; runtime.Gosched(); fmt.Println("b"); channel <- 2 }()
	x := <-channel
	fmt.Println(x)

	// go func() {
	// 	fmt.Print("A1 ")
	// 	channel <- 1
	// 	fmt.Print("A2 ")
	// }()

	// go func() {
	// 	fmt.Print("B1 ")
	// 	x := <-channel
	// 	fmt.Print(x, " ")
	// 	fmt.Print("B2 ")
	// }()

	// go func() {
	// 	fmt.Print("C1 ")
	// 	runtime.Gosched()
	// 	fmt.Print("C2 ")
	// }()

	time.Sleep(100 * time.Millisecond)
	fmt.Println("done")
}
