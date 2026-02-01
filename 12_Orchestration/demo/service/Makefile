
apply:
	kubectl apply -f service.yaml

list_pods:
	kubectl get pods -o wide

list_services:
	kubectl get svc -o wide

delete_pod:
	kubectl delete pod $(POD)

enter_client:
	kubectl exec -it client -- sh

nslookup:
	kubectl exec -it client -- nslookup nginx-service

nslookup_full:
	kubectl exec -it client -- nslookup nginx-service.default.svc.cluster.local

test_service:
	kubectl exec -it client -- wget -O- nginx-service

cleanup:
	kubectl delete -f service.yaml

