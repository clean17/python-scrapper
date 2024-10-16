import requests
import configparser
from yt_dlp import YoutubeDL
import os
import asyncio
import aiohttp

# configparser 초기화
config = configparser.ConfigParser()

# config.ini 파일 읽기
config.read('config.ini')

API_KEY = config['YOUTUBE']['API_KEY']
CHANNEL_USERNAME = 'mojjustice01'
API_URL_CHANNEL = 'https://www.googleapis.com/youtube/v3/channels'
API_URL_SEARCH = 'https://www.googleapis.com/youtube/v3/search'
API_URL_VIDEO_DETAILS = 'https://www.googleapis.com/youtube/v3/videos'
API_URL_COMMENTS = 'https://www.googleapis.com/youtube/v3/commentThreads'

async def download_video(youtube_url):
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
        info_dict = ydl.extract_info(youtube_url, download=True)
        file_path = ydl.prepare_filename(info_dict)  # 파일 경로와 이름 얻기
        return file_path  # 다운로드한 파일의 경로 반환

async def fetch(session, url, params):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error fetching data from {url}: {response.status}")
            return None

async def main():
    async with aiohttp.ClientSession() as session:
        # 1. 채널 ID 가져오기
        channel_params = {
            'part': 'id',
            'forUsername': CHANNEL_USERNAME,
            'key': API_KEY
        }

        channel_data = await fetch(session, API_URL_CHANNEL, channel_params)
        if channel_data:
            channel_id = channel_data['items'][0]['id']
            print(f"Channel ID: {channel_id}")

            # 2. 채널의 동영상 목록 가져오기 (videoId 리스트로 저장)
            video_params = {
                'part': 'snippet',
                'channelId': channel_id,
                'maxResults': 100,
                'order': 'date',
                'type': 'video',
                'key': API_KEY
            }

            video_data = await fetch(session, API_URL_SEARCH, video_params)
            if video_data:
                videos = video_data.get('items', [])

                # videoId를 저장할 리스트 생성
                video_ids = [video['id']['videoId'] for video in videos]

                # 3. videoId로 비디오 메타데이터 가져오기 (비디오 세부 정보 출력)
                for video_id in video_ids:
                    video_details_params = {
                        'part': 'snippet,statistics',
                        'id': video_id,
                        'key': API_KEY
                    }

                    video_details_data = await fetch(session, API_URL_VIDEO_DETAILS, video_details_params)
                    if video_details_data:
                        video_data = video_details_data.get('items', [])[0]
                        snippet = video_data['snippet']
                        statistics = video_data.get('statistics', {})

                        video_title = snippet['title']
                        video_description = snippet['description']
                        video_publish_date = snippet['publishedAt']
                        like_count = statistics.get('likeCount', 'N/A')
                        view_count = statistics.get('viewCount', 'N/A')

                        print(f"Title: {video_title}")
                        print(f"Description: {video_description}")
                        print(f"Published At: {video_publish_date}")
                        print(f"Like Count: {like_count}")
                        print(f"View Count: {view_count}")
                        print(f"URL: https://www.youtube.com/watch?v={video_id}")
                        print("-" * 40)

                        youtube_link = f'https://www.youtube.com/watch?v={video_id}'
                        file_path = await download_video(youtube_link)  # 비디오 다운로드 및 파일 경로 받기
                        print(file_path)

# 비동기 메인 함수 실행
asyncio.run(main())