package main

import (
	"fmt"
	"sync"
)

func main() {
	var r = 0
	var wg sync.WaitGroup
	var mx sync.Mutex

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			mx.Lock()
			r = r + 1
			mx.Unlock()
			wg.Done()
		}()
	}

	wg.Wait()
	fmt.Println(r)
}
