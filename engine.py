import logging

from yt_transcripts import get_transcript

logger = logging.basicConfig()

def run_engine(video_id: str):

    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        transcript = None

    


