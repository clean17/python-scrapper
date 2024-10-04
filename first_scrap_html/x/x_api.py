import requests
import configparser

# configparser 초기화
config = configparser.ConfigParser()

# config.ini 파일 읽기
config.read('config.ini')

# API_KEY = config['X']['API_KEY']
# API_KEY_SECRET = config['X']['API_KEY_SECRET']
# ACCESS_TOKEN = config['X']['ACCESS_TOKEN']
# ACCESS_TOKEN_SECRET = config['X']['ACCESS_TOKEN_SECRET']
BEARER_TOKEN = config['X']['BEARER_TOKEN']


# API 키와 토큰 설정
# consumer_key = API_KEY
# consumer_secret = API_KEY_SECRET
# access_token = ACCESS_TOKEN
# access_token_secret = ACCESS_TOKEN_SECRET
bearer_token = BEARER_TOKEN


# 요청 URL
url = "https://api.twitter.com/2/users/61355799/tweets"
params = {
    'tweet.fields': 'attachments,created_at,public_metrics,text,conversation_id',
    'media.fields': 'media_key,type,url',
    'expansions': 'attachments.media_keys',
    'max_results': '100',
    'pagination_token': '7140dibdnow9c7btw452upzcm8psphs6gh7hr6lsotzxz'
}

# 헤더 설정
headers = {
    'Authorization': f'Bearer {bearer_token}'
}

# 요청 보내기
response = requests.get(url, headers=headers, params=params)

# 결과 출력
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
