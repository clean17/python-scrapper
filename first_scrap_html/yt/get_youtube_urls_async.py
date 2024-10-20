import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import configparser
import os
from playwright.async_api import async_playwright

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

async def scroll_to_bottom(page):
    await page.evaluate("""
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 150; // 스크롤하는 거리
                const timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;

                    if (totalHeight >= document.body.scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 300);
            });
        }
    """)

# 비동기 요청 대신 동기 requests 사용
def fetch(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# YouTube HTML 다운로드
async def download_youtube_html(video_id):
    # YouTube URL 생성
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Playwright 실행
    async with async_playwright() as playwright:
        # headless 모드로 브라우저 실행
        browser = await playwright.chromium.launch(headless=True)  # headless=False로 설정하면 브라우저가 보입니다.
        page = await browser.new_page()

        # YouTube 페이지로 이동
        await page.goto(video_url)
        await scroll_to_bottom(page)

        # HTML 내용 가져오기 (썸네일 및 초기 화면)
        content = page.content()

        # 저장할 디렉토리 생성
        save_dir = 'html'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 파일 경로 생성
        save_path = os.path.join(save_dir, f'youtube_{video_id}.html')

        # HTML 파일 저장
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"HTML이 {save_path}에 저장되었습니다.")

        # 브라우저 닫기
        browser.close()

async def run_in_executor(func, *args):
    # 스레드 풀을 사용하여 비동기 실행을 흉내냄
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result

async def get_channel_id():
    # 1. 채널 ID 가져오기
    channel_params = {
        'part': 'id',
        'forUsername': CHANNEL_USERNAME,
        'key': API_KEY
    }

    # 동기 함수 fetch를 비동기적으로 실행
    channel_data = await run_in_executor(fetch, API_URL_CHANNEL, channel_params)
    if channel_data and 'items' in channel_data:
        return channel_data['items'][0]['id']
    else:
        return None

async def get_video_ids(channel_id):
    # 2. 채널의 동영상 목록 가져오기 (videoId 리스트로 저장)
    video_params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 100,
        'order': 'date',
        'type': 'video',
        'key': API_KEY
    }

    # 동기 함수 fetch를 비동기적으로 실행
    video_data = await run_in_executor(fetch, API_URL_SEARCH, video_params)
    if video_data and 'items' in video_data:
        return [video['id']['videoId'] for video in video_data['items']]
    else:
        return []

async def get_video_details(video_id):
    # 3. videoId로 비디오 메타데이터 가져오기
    video_details_params = {
        'part': 'snippet,statistics',
        'id': video_id,
        'key': API_KEY
    }

    # 동기 함수 fetch를 비동기적으로 실행
    video_data = await run_in_executor(fetch, API_URL_VIDEO_DETAILS, video_details_params)
    if video_data and 'items' in video_data:
        video_item = video_data['items'][0]
        snippet = video_item['snippet']
        statistics = video_item.get('statistics', {})

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

        await download_youtube_html(video_id)

async def main():
    # 채널 ID 가져오기
    channel_id = await get_channel_id()
    if not channel_id:
        print("채널 ID를 가져올 수 없습니다.")
        return

    # 비디오 ID 리스트 가져오기
    video_ids = await get_video_ids(channel_id)
    if not video_ids:
        print("동영상을 가져올 수 없습니다.")
        return

    # 각 비디오 ID에 대해 메타데이터 가져오기
    tasks = []
    for video_id in video_ids:
        tasks.append(get_video_details(video_id))

    # 비동기로 모든 작업 실행
    await asyncio.gather(*tasks)

# 비동기 이벤트 루프 실행
asyncio.run(main())
