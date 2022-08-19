# epsitter
Endpoint Babysitter for Kubernetes.

I created this project to fulfill the following requirements:

1. Monitor my API (http) endpoints from within the k8s cluster
2. Emit metrics for Prometheus
3. Be user friendly

Docs will come soon :)

## Configuration
The `sitter.py` script takes on 1 single argument; a yaml configuration file:

```commandline
urls:
  my_service:
    namespace: qa_workloads
    url: https://my-app.nspace.svc.cluster.local:8080
    timeout: 10
  my_api_test:
    namespace: prod
    url: https://api.nspace.svc.cluster.local:8000/api/whatevs
    auth_user: myUsername
    auth_pass: myPa55word
    method: post
    payload:
      some_parameter: "A value goes here"
      another_parameter: "With a diferent value"
    headers:
        x-my-custom-header: "Lee was here."
```