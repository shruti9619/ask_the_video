import logging

from dotenv import load_dotenv

logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def load_configs():
    logger.info("load configs")

    load_dotenv()

    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT_USEAST")
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY_USEAST")
    os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE")
    os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")

    logger.info("Configs loaded")