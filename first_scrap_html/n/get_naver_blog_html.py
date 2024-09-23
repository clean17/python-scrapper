import asyncio
import requests
import json
from datetime import datetime
from playwright.async_api import async_playwright
import os
from urllib.parse import unquote

# 네이버 블로그 API 호출 및 데이터 처리
def fetch_post_data(blog_id, current_page):
    url = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={blog_id}&currentPage={current_page}&countPerPage=5'
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
                # JSON 데이터를 출력 (str()로 변환하여 출력하거나, 그냥 print)
                # print(json.dumps(data, indent=4))  # dict를 JSON 형식의 문자열로 변환하여 출력
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
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        url = f'https://blog.naver.com/mojjustice/{log_no}'
        await page.goto(url)

        content = await page.content()

        # 날짜 형식을 맞추기
        if not validate_date_format(add_date):
            add_date = datetime.now().strftime('%Y.%m.%d')

        # 파일명 만들기
        file_name = f'html/playwright_{log_no}_{add_date}.html'

        # html 디렉토리가 없는 경우 생성
        if not os.path.exists('html'):
            os.makedirs('html')

        # 파일 저장
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"HTML 소스가 '{file_name}'에 저장되었습니다.")
        await browser.close()

# 날짜 형식 검증
def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y.%m.%d')
        return True
    except ValueError:
        return False

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
            print(log_no)
            add_date = post.get('addDate')
            print(add_date)

            # 날짜 검증 및 HTML 다운로드
#             await download_html(log_no, add_date)

        current_page += 1  # 다음 페이지로 이동

# 비동기 이벤트 루프 실행
asyncio.run(main())
