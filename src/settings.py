import environ
import logging

VERSION = __version__ = '0.1-alpha'

_levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'WARN': logging.WARN,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}

env = environ.Env(
    SERVER_PORT=(int, 8989),
    POLL_INTERVAL=(int, 60),
    LOG_LEVEL=(str, 'INFO'),
    POOL_SIZE=(int, 5),
    REQUEST_TIMEOUT=(int, 15),
    METRIC_PREFIX=(str, 'sitter'),
    LOG_FORMAT=(str, '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
)

METRIC_PREFIX = env('METRIC_PREFIX')
POOL_SIZE = env('POOL_SIZE')
SERVER_PORT = env('SERVER_PORT')
POLL_INTERVAL = env('POLL_INTERVAL')
LOG_LEVEL = _levels[str(env('LOG_LEVEL')).upper()]
LOG_FORMAT = env('LOG_FORMAT')
REQUEST_TIMEOUT = env('REQUEST_TIMEOUT')

