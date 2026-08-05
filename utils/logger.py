import contextvars
import logging
import os
import sys

from pythonjsonlogger import jsonlogger


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


class TalentForgeJsonFormatter(
    jsonlogger.JsonFormatter
):

    def add_fields(
        self,
        log_record,
        record,
        message_dict,
    ):
        super().add_fields(
            log_record,
            record,
            message_dict,
        )

        log_record["timestamp"] = (
            log_record.pop(
                "asctime",
                None,
            )
        )

        log_record["level"] = (
            log_record.pop(
                "levelname",
                None,
            )
        )

        log_record["logger"] = (
            log_record.pop(
                "name",
                None,
            )
        )

        log_record["service"] = (
            "talentforge"
        )


def set_request_id(request_id: str):
    return request_id_context.set(request_id)


def clear_request_id(token):
    request_id_context.reset(token)


def configure_logging():

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        TalentForgeJsonFormatter(
            "%(asctime)s "
            "%(levelname)s "
            "%(name)s "
            "%(request_id)s "
            "%(message)s"
        )
    )

    handler.addFilter(RequestIdFilter())

    root_logger = logging.getLogger()

    log_level = os.getenv(
        "LOG_LEVEL",
        "INFO",
    ).upper()

    root_logger.setLevel(log_level)

    root_logger.handlers.clear()

    root_logger.addHandler(handler)