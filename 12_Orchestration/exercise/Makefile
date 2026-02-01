
containerize_server:
	docker build -t counter-server .
	minikube image load counter-server

apply:
	kubectl apply -f counter.yaml

prepare_client:
	kubectl exec -it client -- pip install requests
	kubectl cp client.py client:/client.py
	kubectl exec -it client -- python /client.py

cleanup:
	kubectl delete -f counter.yaml

