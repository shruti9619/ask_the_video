from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np

video_id = "FgakZw6K1QQ"
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages = ['en'])
print(len(transcript))
print(transcript[-1])
print(np.mean([len(trans['text']) for trans in transcript]))







