import json
import os
from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def transcribe(audio_path: str):
    segments, _ = model.transcribe(audio_path)

    transcript = []

    for segment in segments:
        transcript.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return transcript



def save_transcript(video_id: str, transcript: list):
    os.makedirs("storage/transcripts", exist_ok=True)

    path = f"storage/transcripts/{video_id}.json"

    with open(path, "w") as f:
        json.dump(transcript, f, indent=2)

    return path