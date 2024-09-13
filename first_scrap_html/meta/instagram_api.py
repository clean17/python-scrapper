import requests
import configparser

# configparser 초기화
config = configparser.ConfigParser()

# config.ini 파일 읽기
config.read('config.ini')

access_token = config['INSTAGRAM']['ACCESS_TOKEN']

# 인스타그램 게시글 ID와 액세스 토큰 설정
MEDIA_ID = '18042796553068134'
ACCESS_TOKEN = access_token

# Graph API URL
url = f"https://graph.instagram.com/v20.0/{MEDIA_ID}"
params = {
    'fields': 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp',
    'access_token': ACCESS_TOKEN
}

# API 요청
response = requests.get(url, params=params)
data = response.json()

# 결과 출력
print(data)
