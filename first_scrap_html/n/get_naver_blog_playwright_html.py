import asyncio
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.async_api import async_playwright
from urllib.parse import unquote
import re

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

# 네이버 블로그 API 호출 및 데이터 처리
def fetch_post_data(blog_id, current_page):
    url = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={blog_id}&currentPage={current_page}&countPerPage=30'
    response = requests.get(url)

    if response.status_code == 200:
        # text/plain 형식의 응답을 문자열로 가져오기
        text_data = response.text

        # URL 인코딩된 문자가 있을 수 있으므로 이를 디코딩
        decoded_data = unquote(text_data)

        # 백슬래시 문제 해결 (잘못된 이스케이프 문자 제거)
        fixed_data = decoded_data.replace('\\', '')

        try:
            # 디코딩된 데이터를 JSON으로 변환
            data = json.loads(fixed_data)

            # resultCode가 'S'인지 확인
            if data.get('resultCode') == 'S':
                return data.get('postList', [])
            else:
                print("Error: Invalid resultCode")
                return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print(f"Error: Failed to fetch data from API (Status code: {response.status_code})")
        return None


# HTML 다운로드 및 파일 저장
async def download_html(log_no, add_date):
    async with async_playwright() as playwright:
        await run(playwright, log_no)

# 날짜 형식 검증
def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y.%m.%d')
        return True
    except ValueError:
        return False


# 두 번째 스크립트 (log_no로 페이지 처리)
async def run(playwright, log_no):
    browser = await playwright.chromium.launch(headless=True)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()

    url = f'https://blog.naver.com/PostView.naver?blogId=mojjustice&logNo={log_no}'
    await page.goto(url)

    await scroll_to_bottom(page)

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # <script> 태그 모두 제거
    for script in soup.find_all('script'):
        script.decompose()  # 해당 태그와 내용을 제거

    # 빈칸으로 처리할 유니코드 공백 문자 목록
    EMPTY_CHARACTERS = ['\u200B', '\u200C', '\u200D']  # zero-width space, zero-width non-joiner, etc.

    # <p>와 <span> 태그 중 텍스트 콘텐츠에서 중복 공백을 줄이는 처리
    for tag in soup.find_all(['p', 'span']):
        # 태그 내 텍스트 가져오기
        text_content = tag.get_text()

        # 유니코드 공백 문자 제거
        for empty_char in EMPTY_CHARACTERS:
            text_content = text_content.replace(empty_char, '')

        # 중복된 공백 및 줄바꿈을 하나의 공백으로 변환
        # \s+는 공백(스페이스, 탭, 줄바꿈)을 포함한 모든 공백 문자를 의미
        text_content = re.sub(r'\s+', ' ', text_content).strip()

        # 공백을 정리한 텍스트로 태그의 내용을 업데이트
        tag.string = text_content

    post_list_body = soup.find('div', id='postListBody')

    # 2. 좋아요 수 추출 (class="u_cnt _count")
    like_count_tag = post_list_body.find('span', class_='u_cnt _count') if post_list_body else None
    if like_count_tag:
        like_count = like_count_tag.get_text()
        print(f"Likes: {like_count}")

    # 3. 해시태그 추출 (해시태그는 #이 앞에 붙은 글자)
    hashtags = []
    if post_list_body:
        for tag in post_list_body.find_all('a', href=True):
            if tag.get_text().startswith('#'):
                hashtags.append(tag.get_text())
    print(f"Hashtags: {', '.join(hashtags)}")

    # 5. 작성자 추출 (class="nick" 내부 텍스트)
    author_tag = post_list_body.find('span', class_='nick') if post_list_body else None
    if author_tag:
        author = author_tag.get_text()
        print(f"Author: {author}")

    if post_list_body:
        # <body> 태그 찾기
        body_tag = soup.find('body')

        if body_tag:
            # <body> 태그 내부를 <div id="postListBody">로 교체
            body_tag.clear()  # <body> 내부 내용을 모두 제거
            body_tag.append(post_list_body)  # <div id="postListBody">를 추가

            # <style> 태그 추가하여 중앙 정렬을 위한 CSS 작성
            style_tag = soup.new_tag('style')
            style_tag.string = '''
                body {
                    display: flex;
                    justify-content: center; /* 좌우 중앙 정렬 */
                    align-items: flex-start; /* 세로 정렬: 페이지 상단에서 시작 */
                    min-height: 100vh; /* 전체 화면 높이 사용 */
                    margin: 0;
                }
    
                #postListBody {
                    width: 100%; /* 너비를 100%로 설정하여 부모 요소의 너비를 따라감 */
                    max-width: 1200px; /* 원하는 최대 너비 설정 */
                    margin: 0 auto; /* 자동 여백으로 좌우 중앙 정렬 */
                }
                '''
            soup.head.append(style_tag)  # <head> 태그에 <style> 추가

    # HTML 파일 저장
    if not os.path.exists('html'):
        os.makedirs('html')

    save_path = os.path.join('html', f'playwright_{log_no}.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    await browser.close()


# 메인 함수
async def main():
    blog_id = 'mojjustice'
    current_page = 1

    while True:
        post_list = fetch_post_data(blog_id, current_page)

        if post_list is None or len(post_list) == 0:
            print("No more posts or failed to fetch posts. Exiting loop.")
            break  # 작업 종료

        # 각 post 처리
        for post in post_list:
            log_no = post.get('logNo')
            add_date = post.get('addDate')

            # log_no가 있을 경우 HTML 다운로드
            if log_no:
                await download_html(log_no, add_date)

        current_page += 1  # 다음 페이지로 이동

# 비동기 이벤트 루프 실행
asyncio.run(main())
