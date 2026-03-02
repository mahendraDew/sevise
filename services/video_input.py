import yt_dlp
import ffmpeg
import os

def download_youtube_video(url: str, output_path="storage/videos"):
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def extract_audio(video_path: str, output_dir="storage/audio"):
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(
        output_dir,
        os.path.basename(video_path).replace(".mp4", ".mp3")
    )

    (
        ffmpeg
        .input(video_path)
        .output(audio_path)
        .run(overwrite_output=True)
    )

    return audio_path