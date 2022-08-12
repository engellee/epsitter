from prometheus_client import start_http_server, Summary, Counter
import settings


def make_metric_name(metric):
    return '{}_{}'.format(settings.METRIC_PREFIX, metric)


# Configure all the metrics here
request_time_summary = Summary(make_metric_name('request_time'), 'Total time spent requesting URL.',
                               labelnames=('name', 'method', 'url', 'namespace'))

status_code_counter = Counter(make_metric_name('http_status_code'), 'HTTP Status Code.',
                              labelnames=('name', 'method', 'url', 'status', 'namespace'))





