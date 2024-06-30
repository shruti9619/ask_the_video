import logging

from document_processor import rag_pipeline, setup_vector_store

from yt_transcripts import get_transcript

logger = logging.basicConfig()


def run_engine(video_id: str, query: str):

    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        transcript = None

    if transcript:
        vector_store = setup_vector_store(transcript)
        response = rag_pipeline(vector_store, query)
        return response
