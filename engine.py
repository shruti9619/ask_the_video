import logging

from document_processor import rag_pipeline, setup_vector_store
from yt_transcripts import get_transcript

logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)



def run_engine(video_id: str, query: str):
    logger.info(f"Run engine: Processing video id: {video_id}")

    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        transcript = None

    if transcript:
        vector_store = setup_vector_store(transcript)
        response = rag_pipeline(vector_store, query)
        return response
