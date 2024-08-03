import logging
import logging.config
import os

from dotenv import load_dotenv


def load_configs():
    load_dotenv()
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT_USEAST")
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY_USEAST")
    os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE")
    os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")


def get_logger() -> logging.Logger:
    log_level = "INFO"
    formatting = "[%(levelname)s] %(asctime)s (%(process)d) %(module)s: %(message)s"
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "f": {
                    "format": formatting,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "h": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": log_level,
                }
            },
            "loggers": {"default": {"handlers": ["h"], "level": log_level}},
        }
    )

    return logging.getLogger("default")
