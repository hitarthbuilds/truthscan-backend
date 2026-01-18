import logging
import sys

LOG_FORMAT = (
    "[%(asctime)s] "
    "[%(levelname)s] "
    "[request_id=%(request_id)s] "
    "%(name)s: %(message)s"
)

class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]

    root.addFilter(RequestIdFilter())
