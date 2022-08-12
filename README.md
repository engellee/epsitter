# epsitter
Endpoint Babysitter

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
    url: https://my-app.nspace.svc.cluster.local:8080
    timeout: 10
  my_other_api:
    url: https://api.nspace.svc.cluster.local:8000
```