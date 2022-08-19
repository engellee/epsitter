from __future__ import with_statement
import logging
import os
import prom
import requests
import settings
import sys
from queue import Queue
from threading import Thread
import time
import yaml


class SitterWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue
            url_obj = self.queue.get()
            try:
                do_request(url_obj)
            except:
                logging.exception("Request failed for '%s' URL=%s", url_obj['name'], url_obj['url'])
            finally:
                self.queue.task_done()


def get_config(_config_file):
    if not os.path.exists(_config_file):
        raise Exception("Config file '%s' does NOT exist. Exiting.", _config_file)

    with open(_config_file) as yfh:
        return yaml.safe_load(yfh)


def generate_metrics(_config):
    logging.info("Generating metrics for %s urls.", str(len(config['urls'])))

    queue = Queue()
    for x in range(settings.POOL_SIZE):
        worker = SitterWorker(queue)
        worker.daemon = True  # let the main thread exit even though the workers are blocking
        worker.start()

    # Put the urls into the queue
    for _url in config['urls']:
        config['urls'][_url]['name'] = _url
        queue.put(config['urls'][_url])

    queue.join()  # main thread to wait for the queue to finish processing all urls


def do_request(url_object):
    namespace = 'Unknown'
    auth = None
    method = 'get'
    timeout = settings.REQUEST_TIMEOUT
    headers = {'user-agent': 'epsitter/{}'.format(settings.VERSION)}
    payload = None

    if 'headers' in url_object:
        headers.update(url_object['headers'])

    if 'namespace' in url_object:
        namespace = url_object['namespace']

    if 'timeout' in url_object:
        timeout = url_object['timeout']

    if 'method' in url_object:
        method = url_object['method']

    if 'payload' in url_object:
        payload = url_object['payload']

    if 'auth_user' in url_object:
        if 'auth_pass' in url_object:
            auth = (url_object['auth_user'], url_object['auth_pass'])

    logging.info("Processing '%s' URL=%s METHOD=%s TIMEOUT=%s",
                 url_object['name'], url_object['url'], method, str(timeout))

    request_time_metric = prom.request_time_summary.labels(
        name=url_object['name'],
        method=method,
        url=url_object['url'],
        namespace=namespace
    )

    try:
        # Record the request time
        with request_time_metric.time():
            http_req = requests.request(method, url_object['url'],
                                        timeout=timeout,
                                        headers=headers,
                                        auth=auth,
                                        data=payload)
    except:
        # if we fail, record an error
        logging.exception("Failed to connect to '%s'", url_object['url'])
        prom.http_error_counter.labels(
            name=url_object['name'],
            method=method,
            url=url_object['url'],
            namespace=namespace).inc(1)
    else:
        # record the status code
        if http_req.status_code:
            prom.status_code_counter.labels(
                name=url_object['name'],
                method=method,
                url=url_object['url'],
                status=http_req.status_code,
                namespace=namespace).inc(1)
            logging.debug("Response: url=%s Headers=%s", url_object['url'], http_req.headers)
            logging.debug("Response: url=%s Text=%s", url_object['url'], http_req.text)

    logging.info("Completed processing '%s'.", url_object['name'])


if __name__ == '__main__':
    os.environ['PROMETHEUS_DISABLE_CREATED_SERIES'] = str(settings.PROMETHEUS_DISABLE_CREATED_SERIES)

    config_file = 'sitter.yaml'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    config = get_config(config_file)

    logging.basicConfig(format=settings.LOG_FORMAT,
                        level=settings.LOG_LEVEL,
                        stream=sys.stderr)

    logging.info("Starting up: %s", sys.argv)
    logging.info("Config: %s", config_file)

    logging.debug("LOG_LEVEL=%s", settings.LOG_LEVEL)
    logging.debug("POLL_INTERVAL=%s", settings.POLL_INTERVAL)
    logging.debug("SERVER_PORT=%s", settings.SERVER_PORT)
    logging.debug("POOL_SIZE=%s", settings.POOL_SIZE)

    # Start up the server to expose the metrics.
    prom.start_http_server(settings.SERVER_PORT)

    # Generate some metrics.
    while True:
        generate_metrics(config)
        time.sleep(settings.POLL_INTERVAL)
