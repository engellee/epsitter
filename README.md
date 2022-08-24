# epsitter
Endpoint Babysitter for Kubernetes.

I created this project to fulfill the following requirements:

1. Monitor my API (http) endpoints from within the k8s cluster
2. Emit metrics for Prometheus
3. Be user friendly

## Configuration
The `sitter.py` script takes on 1 single argument; a YAML configuration file:

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

## Environment Variables

| Env Variable | Default | Description                          |
|--------------|---------|--------------------------------------|
| LOG_LEVEL | `INFO` | Log level.                           |
| POLL_INTERVAL | `30` | How often to test targets (seconds). |
| SERVER_PORT | `8989` | Which port to bind to.               |
| POOL_SIZE | `5` | Number of worker threads.            |
| REQUEST_TIMEOUT | `15` | Global request timeout.              |
| METRIC_PREFIX | `sitter` | Metric name prefix.                  |

## Metrics

[Prometheus Metrics Types](https://prometheus.io/docs/concepts/metric_types/)

| Metric                   | Type | Labels                                     | Description                 |
|--------------------------| ---- |--------------------------------------------|-----------------------------|
| `sitter_request_time`    | Summary | `name` `method` `url`  `namespace`         | HTTP request time.          |
| `sitter_http_status_code` | Counter | `name` `method` `url`  `namespace` `status` | Count of HTTP status codes. |
| `sitter_http_error`       | Counter |  `name` `method` `url`  `namespace` | Count of connection errors. |

## Building

[GitHub Actions](./.github/workflows/) usesd to build the container image.

[epsitter on DockerHub](https://hub.docker.com/repository/docker/lsengel/epsitter)
