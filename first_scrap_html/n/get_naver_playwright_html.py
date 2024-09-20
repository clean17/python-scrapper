import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

async def scroll_to_bottom(page):
    await page.evaluate("""
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100; // 스크롤하는 거리
                const timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;

                    if (totalHeight >= document.body.scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 40);
            });
        }
    """)

async def run(playwright):
    #     browser = await playwright.chromium.launch()
    browser = await playwright.chromium.launch(headless=False)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()
    await page.goto('https://blog.naver.com/PostView.naver?blogId=mojjustice&logNo=223456814936')
    await page.goto('https://blog.naver.com/PostView.naver?blogId=mojjustice&logNo=223579226685')
    #     await page.wait_for_load_state('networkidle')  # 네트워크 요청이 완전히 끝날 때까지 대기 - 스켈레톤으로 나온다

    await scroll_to_bottom(page)
    #     await page.screenshot(path="full_page_screenshot.png", full_page=True)

    content = await page.content()
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')

    # <script> 태그 모두 제거
    for script in soup.find_all('script'):
        script.decompose()  # 해당 태그와 내용을 제거

    """ # <div id="postListBody">를 찾기
    post_list_body = soup.find('div', id='postListBody')

    if post_list_body:
        # <body> 태그 찾기
        body_tag = soup.find('body')

        if body_tag:
            # <body> 태그 내부를 <div id="postListBody">로 교체
            body_tag.clear()  # <body> 내부 내용을 모두 제거
            body_tag.append(post_list_body)  # <div id="postListBody">를 추가 """

    # <div id="postListBody">를 찾기
    post_list_body = soup.find('div', id='postListBody')

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

    save_path = os.path.join('html', 'playwright_naver.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    title = await page.title()
    print(f"Page title: {title}")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())