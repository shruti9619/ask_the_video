from youtube_transcript_api import YouTubeTranscriptApi

from setup_configs import get_logger

logger = get_logger()

def process_transcript(transcript: list, num_chunk_combine:int = 15) -> list:
    new_chunks = []
    for i in range(0, len(transcript), num_chunk_combine):
        new_chunks.append({"text":" ".join([chunk['text'] for chunk in transcript[i:i+num_chunk_combine]])})
    
    return new_chunks


def get_transcript(video_id: str) -> list:
    logger.info(f"Getting transcript for video id: {video_id}")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"]
        )
        logger.info(
            f"Transcript for video id: {video_id} with length {len(transcript)} \
                     fetched successfully"
        )

        transcript = process_transcript(transcript= transcript)
        return transcript

    except Exception as e:
        logger.error(f"Error while fetching transcript for video id: {video_id}")
        logger.error(e)
        raise Exception(f"Error while fetching transcript for video id: {video_id}")
