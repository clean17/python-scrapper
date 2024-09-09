import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# 스크래핑할 Instagram 페이지 URL
url = 'https://www.instagram.com/ministry_of_justice_korea/'

# HTTP 요청 보내기
response = requests.get(url)

# 페이지 콘텐츠 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# Instagram 페이지에 포함된 JavaScript 데이터 추출
scripts = soup.find_all('script', type="text/javascript")

# 필요한 데이터를 포함하는 script 요소 찾기
shared_data = None
for script in scripts:
    if 'window._sharedData =' in script.text:
        json_data = script.text.split('window._sharedData = ')[1][:-1]
        shared_data = json.loads(json_data)
        break

# 게시글 데이터 추출
posts_data = []
if shared_data:
    # 페이지의 게시글 정보가 포함된 섹션
    user_data = shared_data['entry_data']['ProfilePage'][0]['graphql']['user']
    posts = user_data['edge_owner_to_timeline_media']['edges']

    # 게시글 URL 및 기타 정보 수집
    for post in posts:
        node = post['node']
        post_url = f"https://www.instagram.com/p/{node['shortcode']}/"
        post_caption = node['edge_media_to_caption']['edges'][0]['node']['text'] if node['edge_media_to_caption']['edges'] else ''
        post_timestamp = node['taken_at_timestamp']
        post_likes = node['edge_liked_by']['count']
        posts_data.append([post_url, post_caption, post_timestamp, post_likes])

# DataFrame으로 변환하여 엑셀로 저장
df = pd.DataFrame(posts_data, columns=['Post URL', 'Caption', 'Timestamp', 'Likes'])
df.to_excel('instagram_posts.xlsx', index=False)

print("Instagram 게시글 정보를 엑셀 파일로 저장했습니다.")
