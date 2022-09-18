import logging
import sys

from pythonjsonlogger import jsonlogger

from app.middleware import get_request_id


class AppFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True


def setup_logging():
    logger = logging.getLogger()
    syslog = logging.StreamHandler(stream=sys.stdout)
    syslog.addFilter(AppFilter())

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(request_id)s %(name)s %(message)s"
    )
    syslog.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(syslog)
    return logger
