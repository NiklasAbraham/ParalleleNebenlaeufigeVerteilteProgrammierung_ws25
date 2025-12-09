package main

import (
	"fmt"
	"math/rand"
	"sync"
)

var accounts [10000]int
var mutex sync.Mutex

func transfer(amount int, source int, target int) bool {
	mutex.Lock()
	if accounts[source] < amount {
	  mutex.Unlock()
		return false
	}
	accounts[source] = accounts[source] - amount
	accounts[target] = accounts[target] + amount
	mutex.Unlock()
	return true
}

func main() {

	for i := range accounts {
		accounts[i] = 1000
	}

	var wg sync.WaitGroup

	for i:= range 1000000 {
		random := rand.New(rand.NewSource(int64(i)))
		source := random.Intn(len(accounts))
		target := random.Intn(len(accounts))
		amount := random.Intn(1000)
		wg.Add(1)
		go func() {
			for !transfer(amount, source, target) { }
			wg.Done()
		}()
		wg.Add(1)
		go func() {
			for !transfer(amount, target, source) { }
			wg.Done()
		}()

	}

	wg.Wait()

	total := 0
	for i := range accounts {
		total = total + accounts[i]
	}

	fmt.Printf("Total: %d\n", total)
}

