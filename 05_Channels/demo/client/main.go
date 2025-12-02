package main

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
)

func main() {
	ch1 := make(chan int)
	ch2 := make(chan int)

	go func() { ch1 <- fetch(8001) }()
	go func() { ch2 <- fetch(8002) }()

	fmt.Println(<-ch1 + <-ch2)
}

func fetch(port int) int {
	resp, _ := http.Get(fmt.Sprintf("http://localhost:%d", port))
	body, _ := io.ReadAll(resp.Body)
	n, _ := strconv.Atoi(string(body))
	resp.Body.Close()
	return n
}
