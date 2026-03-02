def chunk_transcript(transcript, window=30):
    chunks = []
    current_chunk = []
    chunk_start = transcript[0]["start"]

    for segment in transcript:
        current_chunk.append(segment["text"])

        if segment["end"] - chunk_start >= window:
            chunks.append({
                "text": " ".join(current_chunk),
                "start_time": chunk_start,
                "end_time": segment["end"]
            })

            current_chunk = []
            chunk_start = segment["end"]

    return chunks