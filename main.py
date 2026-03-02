import asyncio
from services.yt_vid_downloader import YoutubeDownloader
from services.speech_recognizer import SpeechRecognition
import subprocess
from services.semantic_search import SemanticSearching
from services.rag import TranscriptRAGAgent
def main(): 
    # task 1: download yt video
    print("TASK 1: Downloading youtube video...")
    yt_downloader = YoutubeDownloader()
    # yt_link_input = input("Enter yt link: ")
    # yt_link = "https://www.youtube.com/watch?v=8of5w7RgcTc";
    yt_link_py_1min = "https://www.youtube.com/watch?v=vE7Cy5csYbQ"
    
    title = yt_downloader.download_video(yt_link_py_1min, "downloads")
    print(f"DONE: downloaded yt video: {title}")


    # task 2: yt video extract the transcript from downloaded vid
    print("TASK 2: Transcribing the downloaded video...")
    video_path = f"downloads/{title}.mp4"
    # video_path = f"downloads/Python in 2 Minutes!.mp4"
    print("TASK 2.1: extracting audio...")
    sr = SpeechRecognition()

    audio_path = sr.extract_audio(video_path)
    print("DONE 2.1: extracted the audio...")
    # transcript = sr.transcribe_audio(audio_path)
    print("TASK 2.2: extracting text from audio...")
    transcript_ts = sr.transcribe_with_timestamps(audio_path)  # 30s per chunk
    print("DONE 2.2: extracted the text...")
    print("-----------------------------------")
    # print("Transcript:\n", transcript_ts)


    if transcript_ts:
        print('transcript found.')
        controller(transcript_ts, video_path)
        

    else:
        print("Unable to download transcript.")


def open_video_at_timestamp(video_path, seconds):
    """Open video in VLC at a specific timestamp"""
    try:
        subprocess.run(["vlc", f"--start-time={seconds}", video_path])
    except FileNotFoundError:
        print("VLC not found! Please install VLC or add it to PATH.")


def controller(transcript, vid_path):
    while True:
        print("\n")
        print("1. search for a specific phrase and get timestamp?")
        print("2. semantic search")
        print("3. RAG search/gen")
        print("4. to exit.")
        raw = input("Enter 1, 2 and 3 or 4 to exit: ").strip()
        try:
            option = int(raw)
        except ValueError:
            print(f"Invalid input: {raw!r}. Please enter 1, 2, 3, or 4.")
            continue

        if option == 4:
            break
        if option == 1:
            sr = SpeechRecognition()

            search_topic = input("Enter a keyword to search: ")
            # try:
            #     for res in results:
            #         print(f"[{res['timestamp']}] {res['text']}")
            #         print(f"Link: {res['yt_link']}\n")
            #     print("Task 2: timestamp(s):")
            print("")
            print('Task 3 : searching for query: ', search_topic)
            results = sr.search_transcript(transcript, search_topic)
            # print("results: ", results)
            # for text, ts,  in results:
            #     print(f"Found at {ts} -> Snippet: {text} \n")


            for match in results:
                # print(match)
                if isinstance(match, dict): 
                    print(f"Found at {match['timestamp']} -> {match['snippet']}")
                    print("\n")
                    choice = input(f"Open video at {match['timestamp']}? (y/n): ")
                    if choice.lower() == "y":
                        open_video_at_timestamp(vid_path, match["seconds"])
                else:
                    # match is probably a string (error or no result)
                    print(match)
                # if "error" in match:
                #     print(match["error"])
                # else:
                #     print("this is match::::", match)
                #     print(f"Found at {match['timestamp']} -> {match['snippet']}")
                #     print("\n")
                #     choice = input(f"Open video at {match['timestamp']}? (y/n): ")
                #     if choice.lower() == "y":
                #         open_video_at_timestamp(vid_path, match["seconds"])
       
        
        elif option == 2:
            print("")
            print('Task 4 : semantic search')
            search_query = input("Enter a query to search: ")

        #     #perform a semantic search
            sem_searching = SemanticSearching()
            asyncio.run(sem_searching.semanticSearch(transcript, search_query))
        elif option == 3:
            print("")
            print('Task 4 : rag search')
            search_query = input("Enter a query to search: ")

            #perform a semantic search
            rag_agent = TranscriptRAGAgent()
            rag_agent.create_agent(transcript, search_query)

        else:
            break

if __name__ == "__main__":
    main()