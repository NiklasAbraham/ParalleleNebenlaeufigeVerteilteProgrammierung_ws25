network:
	kubectl apply -f demo/network.yaml

list_address:
	kubectl get pods -o wide

enter_a:
	kubectl exec -it two-containers -c container-a -- sh

enter_b:
	kubectl exec -it two-containers -c container-b -- sh

cleanup:
	kubectl delete -f network.yaml

network_server:
	nc -l -p 8080

network_client:
	nc localhost 8080

