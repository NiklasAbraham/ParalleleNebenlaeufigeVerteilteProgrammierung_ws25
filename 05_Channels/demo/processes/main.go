package main

import "fmt"
import "time"
import "runtime"

func main() {

	go func() { fmt.Print("A1 "); runtime.Gosched(); fmt.Print("A2 ") }()
	go func() { fmt.Print("B1 "); runtime.Gosched();fmt.Print("B2 ") }()
	go func() { fmt.Print("C1 "); runtime.Gosched();fmt.Print("C2 ") }()

	time.Sleep(100 * time.Millisecond)

	fmt.Println()
}
