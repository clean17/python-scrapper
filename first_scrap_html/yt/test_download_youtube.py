from yt_dlp import YoutubeDL
import requests
import os

def download_video(youtube_url):
    video_directory = 'video'
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'verbose': True,  # Verbose 모드 활성화
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'outtmpl': os.path.join(video_directory, '%(title)s.%(ext)s')
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
        info_dict = ydl.extract_info(youtube_url, download=False)
        file_path = ydl.prepare_filename(info_dict)  # 파일 경로와 이름 얻기
        return file_path  # 다운로드한 파일의 경로 반환

def upload_file(file_path, upload_url):
    files = {'file': open(file_path, 'rb')}  # 파일을 바이너리 읽기 모드로 열기
    response = requests.post(upload_url, files=files)  # 파일과 함께 POST 요청 보내기
    return response

youtube_link = 'https://www.youtube.com/watch?v=0UsQJWybmxE'
file_path = download_video(youtube_link)  # 비디오 다운로드 및 파일 경로 받기

# upload_url = 'https://yourserver.com/upload'  # 파일을 업로드할 서버의 URL
# response = upload_file(file_path, upload_url)
# print("Upload response:", response.text)