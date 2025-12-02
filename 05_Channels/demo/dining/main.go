package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	fork0 := &sync.Mutex{}
	fork1 := &sync.Mutex{}
	fork2 := &sync.Mutex{}
	fork3 := &sync.Mutex{}
	fork4 := &sync.Mutex{}

	var wg sync.WaitGroup
	wg.Add(5)

	waiter := make(chan bool, 4)

	go func() {
		waiter <- true
		fork0.Lock(); time.Sleep(1000000); fork1.Lock()
		fmt.Println("0 eating"); fork0.Unlock(); fork1.Unlock()
		<-waiter
		wg.Done()
	}()

	go func() {
		waiter <- true
		fork1.Lock(); time.Sleep(1000000); fork2.Lock()
		fmt.Println("1 eating"); fork1.Unlock(); fork2.Unlock()
		<-waiter
		wg.Done()
	}()

	go func() {
		waiter <- true
		fork2.Lock(); time.Sleep(1000000); fork3.Lock()
		fmt.Println("2 eating"); fork2.Unlock(); fork3.Unlock()
		<-waiter
		wg.Done()
	}()

	go func() {
		waiter <- true
		fork3.Lock(); time.Sleep(1000000); fork4.Lock()
		fmt.Println("3 eating"); fork3.Unlock(); fork4.Unlock()
		<-waiter
		wg.Done()
	}()

	go func() {
		waiter <- true
		fork4.Lock(); time.Sleep(1000000); fork0.Lock()
		fmt.Println("4 eating"); fork4.Unlock(); fork0.Unlock()
		<-waiter
		wg.Done()
	}()

	wg.Wait()
}
