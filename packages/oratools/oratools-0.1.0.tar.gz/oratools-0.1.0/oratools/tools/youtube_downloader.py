import os
from pytube import YouTube

def download_youtube_video(url, output_path=None):
    try:
        if not output_path:
            output_path = os.getcwd()
        
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        file_path = video.download(output_path)
        
        return file_path
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

def download_youtube_audio(url, output_path=None):
    try:
        if not output_path:
            output_path = os.getcwd()
        
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        file_path = audio.download(output_path)
        
        base, _ = os.path.splitext(file_path)
        new_file_path = f"{base}.mp3"
        os.rename(file_path, new_file_path)
        
        return new_file_path
    except Exception as e:
        raise Exception(f"Failed to download audio: {str(e)}") 