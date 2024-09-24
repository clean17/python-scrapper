import requests
import configparser

# configparser 초기화
config = configparser.ConfigParser()

# config.ini 파일 읽기
config.read('config.ini')

API_KEY = config['YOUTUBE']['API_KEY']
CHANNEL_USERNAME = 'mojjustice01'
API_URL_CHANNEL = 'https://www.googleapis.com/youtube/v3/channels'
API_URL_SEARCH = 'https://www.googleapis.com/youtube/v3/search'
API_URL_VIDEO_DETAILS = 'https://www.googleapis.com/youtube/v3/videos'

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

    # 2. 채널의 동영상 목록 가져오기 (videoId 리스트로 저장)
    video_params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 100,
        'order': 'date',
        'type': 'video',
        'key': API_KEY
    }

    video_response = requests.get(API_URL_SEARCH, params=video_params)
    if video_response.status_code == 200:
        videos = video_response.json().get('items', [])

        # videoId를 저장할 리스트 생성
        video_ids = [video['id']['videoId'] for video in videos]

        # 3. videoId로 비디오 메타데이터 가져오기 (비디오 세부 정보 출력)
        for video_id in video_ids:
            video_details_params = {
                'part': 'snippet,statistics',  # snippet과 statistics 같이 가져옴
                'id': video_id,
                'key': API_KEY
            }

            video_details_response = requests.get(API_URL_VIDEO_DETAILS, params=video_details_params)
            if video_details_response.status_code == 200:
                video_data = video_details_response.json().get('items', [])[0]
                snippet = video_data['snippet']
                statistics = video_data.get('statistics', {})

                video_title = snippet['title']
                video_description = snippet['description']
                video_publish_date = snippet['publishedAt']
                like_count = statistics.get('likeCount', 'N/A')  # 좋아요 수가 없으면 N/A
                view_count = statistics.get('viewCount', 'N/A')  # 조회수

                print(f"Title: {video_title}")
                print(f"Description: {video_description}")
                print(f"Published At: {video_publish_date}")
                print(f"Like Count: {like_count}")
                print(f"View Count: {view_count}")
                print(f"URL: https://www.youtube.com/watch?v={video_id}")
                print("-" * 40)
            else:
                print(f"Error fetching video details for {video_id}: {video_details_response.status_code}")
    else:
        print(f"Error fetching videos: {video_response.status_code}")
else:
    print(f"Error fetching channel ID: {channel_response.status_code}")
