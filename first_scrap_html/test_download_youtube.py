from pytube import YouTube
from pytube.exceptions import VideoUnavailable

def download_video(video_url):
    try:
        yt = YouTube(video_url)
        yt.streams.filter(adaptive=True, file_extension='mp4').first().download()
        print(f"Downloaded: {yt.title}")
    except VideoUnavailable:
        print(f"Video {video_url} is unavailable.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=Mj7Y6sY2DWk'
    download_video(video_url)
