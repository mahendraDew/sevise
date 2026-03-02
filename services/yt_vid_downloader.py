
import yt_dlp
import time
class YoutubeDownloader: 

    def download_video(self, url: str, path: str = ".") -> str:
        try: 
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',   # best video + best audio
                'merge_output_format': 'mp4',           # force mp4 after merging
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'             # ensure conversion to mp4
                }]
            }
            title = ""
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title')
                print(f"Downloaded: {title}")
                
            return title

        except Exception as e:
            raise RuntimeError(f"Unable to download yt video: {e}") from e

