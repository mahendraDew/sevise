# import speech_recognition
import pyttsx3

import subprocess
import speech_recognition as sr
import difflib
class SpeechRecognition:
   


    def extract_audio(self, video_file, audio_file="audio.wav"):
        # Use ffmpeg to convert video → wav
        command = ["ffmpeg", "-y", "-i", video_file, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_file]
        subprocess.run(command, check=True)
        return audio_file

    def transcribe_audio(self, audio_file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)  # Load the whole audio

        try:
            text = recognizer.recognize_google(audio)  # Uses Google Web Speech API
            return text
        except sr.UnknownValueError:
            return "Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google API; {e}"



    def transcribe_with_timestamps(self, audio_file, chunk_length=7):
        recognizer = sr.Recognizer()
        transcript = []

        with sr.AudioFile(audio_file) as source:
            duration = int(source.DURATION)
            print(f"Audio length: {duration} seconds")

            for i in range(0, duration, chunk_length):
                start = i
                end = min(i + chunk_length, duration)

                audio = recognizer.record(source, duration=chunk_length)  # sequential read

                try:
                    text = recognizer.recognize_google(audio)
                    transcript.append({"start": start, "end": end, "text": text})
                    print(f"[{start}-{end}s]: {text}")
                except sr.UnknownValueError:
                    transcript.append({"start": start, "end": end, "text": "Unintelligible"})
                except sr.RequestError as e:
                    transcript.append({"start": start, "end": end, "text": f"API error: {e}"})

        return transcript
    
    def search_transcript(self, transcript, query, threshold = 0.6):
        try: 
            query = query.lower()
            matches = []

            for snippet in transcript.snippets:
                words = snippet.text.lower().split()
                for word in words:
                    similarity = difflib.SequenceMatcher(None, query, word).ratio()
                    if similarity >= threshold:  # fuzzy match
                        ts = int(snippet.start)
                        mins, secs = divmod(ts, 60)
                        timestamp = f"{mins:02d}:{secs:02d}"
                        # yt_link = f"https://www.youtube.com/watch?v={video_id}&t={ts}s"
                        matches.append((snippet.text, timestamp))
                        break  # avoid duplicate match for same snippet

            if not matches:
                return [f"Sorry, no results found for query: '{query}'"]

            return matches
        except Exception as e:
            return [f"Error while searching transcript: {str(e)}"]

    def search_transcript(self, transcript, query, threshold=0.6):
        try:
            query = query.lower()
            matches = []

            for snippet in transcript:  # transcript is now a list of dicts
                words = snippet["text"].lower().split()
                for word in words:
                    similarity = difflib.SequenceMatcher(None, query, word).ratio()
                    if similarity >= threshold:  # fuzzy match
                        ts = int(snippet["start"])
                        mins, secs = divmod(ts, 60)
                        timestamp = f"{mins:02d}:{secs:02d}"
                        # matches.append((snippet["text"], timestamp, ts))
                        matches.append({
                            "snippet": snippet["text"],
                            "timestamp": timestamp,
                            "seconds": ts
                        })
                        break  # avoid duplicate match for same snippet

            if not matches:
                return [f"Sorry, no results found for query: '{query}'"]

            return matches
        except Exception as e:
            return [f"Error while searching transcript: {str(e)}"]
