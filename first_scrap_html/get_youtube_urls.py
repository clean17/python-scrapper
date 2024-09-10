import requests
import configparser

# configparser 초기화
config = configparser.ConfigParser()

# config.ini 파일 읽기
config.read('config.ini')

API_KEY = config['DEFAULT']['API_KEY']
CHANNEL_USERNAME = 'mojjustice01'
API_URL_CHANNEL = 'https://www.googleapis.com/youtube/v3/channels'
API_URL_VIDEOS = 'https://www.googleapis.com/youtube/v3/search'

# 1. 채널 ID 가져오기
channel_params = {
    'part': 'id',
    'forUsername': CHANNEL_USERNAME,
    'key': API_KEY
}

channel_response = requests.get(API_URL_CHANNEL, params=channel_params)
if channel_response.status_code == 200:
    channel_data = channel_response.json()
    channel_id = channel_data['items'][0]['id']
    print(f"Channel ID: {channel_id}")

    # 2. 채널의 동영상 목록과 메타데이터 가져오기
    video_params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 100,  # 최대 10개의 동영상 가져오기
        'order': 'date',   # 최신 순으로 정렬
        'type': 'video',
        'key': API_KEY
    }

    video_response = requests.get(API_URL_VIDEOS, params=video_params)
    if video_response.status_code == 200:
        videos = video_response.json().get('items', [])

        for video in videos:
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            video_description = video['snippet']['description']
            video_publish_date = video['snippet']['publishedAt']
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            print(f"Title: {video_title}")
            print(f"Description: {video_description}")
            print(f"Published At: {video_publish_date}")
            print(f"URL: {video_url}")
            print("-" * 40)
    else:
        print(f"Error fetching videos: {video_response.status_code}")
else:
    print(f"Error fetching channel ID: {channel_response.status_code}")