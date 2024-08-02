import logging

from document_processor import rag_pipeline, setup_vector_store
from yt_transcripts import get_transcript
import init_llm

logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def load_llm_model(model_type:str = 'HF'):
    logger.info("Setting up LLM Model")

    if model_type == 'HF':
        return init_llm.init_huggingface_llm()

    if model_type =='OAI':
        return init_llm.init_openai_llm()


def run_engine(video_id: str, query: str):
    logger.info(f"Run engine: Processing video id: {video_id}")

    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        transcript = None

    if transcript:

        try:
            llm = load_llm_model()
        except Exception as e:
            logger.error("Error while loading LLM model")
            logger.error(e)
            return []

        vector_store = setup_vector_store(transcript)
        response = rag_pipeline(vector_store, query, llm)
        return response
    else:
        logger.error("failure in fetching transcript")




