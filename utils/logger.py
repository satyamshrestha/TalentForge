import contextvars
import logging


request_id_context = contextvars.ContextVar(
    "request_id",
    default="-",
)


class RequestIdFilter(logging.Filter):

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        record.request_id = request_id_context.get()
        return True


def set_request_id(request_id: str):
    return request_id_context.set(request_id)


def clear_request_id(token):
    request_id_context.reset(token)


def configure_logging():

    handler = logging.StreamHandler()

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "request_id=%(request_id)s | "
            "%(message)s"
        )
    )

    handler.addFilter(RequestIdFilter())

    root_logger = logging.getLogger()

    root_logger.setLevel(logging.INFO)

    root_logger.handlers.clear()

    root_logger.addHandler(handler)