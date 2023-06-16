import os
import youtube_dl

def download_audio(url):
    output_dir = os.path.expanduser("~/Downloads")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Specify output file path
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        ydl.download([info_dict['webpage_url']])

youtube_url = input("Enter URL here: ")
download_audio(youtube_url)
