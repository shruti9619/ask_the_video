from typing import List, Dict, Tuple

from langchain.retrievers import EnsembleRetriever

from document_processor import rag_pipeline, populate_vector_store
from yt_transcripts import get_transcript
import init_llm
from setup_configs import get_logger


logger = get_logger()


def load_retriever(transcript: List) -> EnsembleRetriever:
    """
    Load the retriever

    Args:
        transcript (List): List of transcripts

    Returns:
        EnsembleRetriever: Ensemble retriever
    """
    return populate_vector_store(transcript)


def load_llm_model(model_type: str = "OAI"):
    """
    Load the language model

    Args:
        model_type (str, optional): Model type. Defaults to 'OAI'.

    Returns:
        Language model
    """
    logger.info("Setting up LLM Model")

    if model_type == "HF":
        return init_llm.init_huggingface_llm()

    if model_type == "OAI":
        return init_llm.init_openai_llm()


def load_transcripts(video_id: str) -> List:
    """
    Load the transcripts for the video

    Args:
        video_id (str): Video ID

    Returns:
        list: List of transcripts
    """
    logger.info(f"load_transcripts: Processing video id: {video_id}")
    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        transcript = []
        logger.error("failure in fetching transcript")
    return transcript


def run_engine(
    llm, retriever, query: str, chat_history: List[Dict] = None
) -> tuple[str, bool]:
    """
    Run the engine

    Args:
        llm: Language model
        retriever: Ensemble retriever
        query (str): User query
        chat_history (List[Dict], optional): Chat history. Defaults to None.

    Returns:
        str: Response
        bool: Success flag
    """

    logger.info(f"Run engine")
    success_flag = False
    try:
        response = rag_pipeline(retriever, query, llm, chat_history)
        success_flag = True
    except Exception as e:
        logger.error(f"engine failed for query: {query} with exception {e}")
        success_flag = False
    return response, success_flag
