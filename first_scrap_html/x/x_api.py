import tweepy
import configparser

# configparser 초기화
config = configparser.ConfigParser()

# config.ini 파일 읽기
config.read('config.ini')

API_KEY = config['X']['API_KEY']
API_KEY_SECRET = config['X']['API_KEY_SECRET']
ACCESS_TOKEN = config['X']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['X']['ACCESS_TOKEN_SECRET']
BEARER_TOKEN = config['X']['BEARER_TOKEN']


# API 키와 토큰 설정
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'
consumer_key = API_KEY
consumer_secret = API_KEY_SECRET
bearer_token = BEARER_TOKEN
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

'''
# 트위터 API 인증
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# 특정 공공기관의 트윗 가져오기
public_tweets = api.user_timeline(screen_name='public_institution_handle', count=10)
public_tweets = api.user_timeline(screen_name='happymoj', count=10)

# 트윗 출력
for tweet in public_tweets:
    print(tweet.text)
'''

client = tweepy.Client(bearer_token=bearer_token)

response = client.get_users_tweets(id='happymoj', max_results=10)

# 트윗 출력
for tweet in public_tweets:
    for tweet in response.data:
        print(tweet.text)