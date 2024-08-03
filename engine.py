from document_processor import rag_pipeline, populate_vector_store
from yt_transcripts import get_transcript
import init_llm

from setup_configs import get_logger

logger = get_logger()


def load_vector_store(transcript: list):
    return populate_vector_store(transcript)

def load_llm_model(model_type:str = 'OAI'):
    logger.info("Setting up LLM Model")

    if model_type == 'HF':
        return init_llm.init_huggingface_llm()

    if model_type =='OAI':
        return init_llm.init_openai_llm()

def load_transcripts(video_id:str) -> list:
    logger.info(f"load_transcripts: Processing video id: {video_id}")
    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        transcript = []
        logger.error("failure in fetching transcript")
    return transcript


def run_engine(llm, vector_store, query: str):
    logger.info(f"Run engine")
    success_flag = False
    try:
        response = rag_pipeline(vector_store, query, llm)
        success_flag = True
    except Exception as e:
        logger.error(f"engine failed for query: {query} with exception {e}")
        success_flag = False
    return response, success_flag





