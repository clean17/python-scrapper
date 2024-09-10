import tweepy

# API 키와 토큰 설정
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# 트위터 API 인증
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# 특정 공공기관의 트윗 가져오기
public_tweets = api.user_timeline(screen_name='public_institution_handle', count=10)

# 트윗 출력
for tweet in public_tweets:
    print(tweet.text)