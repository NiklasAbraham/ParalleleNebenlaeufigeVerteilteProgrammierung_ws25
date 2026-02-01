apply:
	kubectl apply -f autoscaling.yaml

list_pods:
	kubectl get pods

list_hpa:
	kubectl get hpa

watch_hpa:
	kubectl get hpa --watch

generate_load:
	kubectl run -it load-generator --rm --image=busybox --restart=Never -- sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"

cleanup:
	kubectl delete -f autoscaling.yaml

