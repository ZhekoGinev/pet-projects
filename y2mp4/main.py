import os
import youtube_dl


def download_video(url):
    output_dir = os.path.expanduser("~/Downloads")
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


youtube_url = input("Enter URL here: ")
download_video(youtube_url)
