# Exercise 12: Orchestration

## Replicated Counter

Deploy a replicated counter service that maintains a single integer state among
three replicas. The server `server.py` has endpoints `get` and `put` and is
replicated three times. The client in file `client.py` sends put operations to
all three replicas and get operations to one of them. Deploy the distributed
system with the following steps:

```
minikube start

docker build -t counter-server .

minikube image load counter-server

kubectl apply -f counter.yaml

kubectl wait --for=condition=ready pod/client --timeout=60s

kubectl exec -it client -- pip install requests

kubectl cp client.py client:/client.py

kubectl exec -it client -- python /client.py

kubectl delete -f counter.yaml
```

Find out what each of them does. Then add an `increment` endpoint to the server
and make it usable from the client. Redeploy the distributed system by following
the same steps and adjusting them if necessary.

