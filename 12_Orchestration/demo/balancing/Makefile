apply:
	kubectl apply -f balancing.yaml

list_pods:
	kubectl get pods -o wide

list_services:
	kubectl get svc -o wide

enter_client:
	kubectl exec -it client -- sh

test_once:
	kubectl exec -it client -- wget -qO- whoami-service

test_multiple:
	kubectl exec -it client -- sh -c 'for i in 1 2 3 4 5; do wget -qO- whoami-service | grep Hostname; done'

cleanup:
	kubectl delete -f balancing.yaml

