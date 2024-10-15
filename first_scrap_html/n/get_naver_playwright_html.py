import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

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

async def run(playwright):
    #     browser = await playwright.chromium.launch()
    browser = await playwright.chromium.launch(headless=False)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()
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

    # 2. 좋아요 수 추출 (class="u_cnt _count")
    like_count_tag = post_list_body.find('span', class_='u_cnt _count')
    if like_count_tag:
        like_count = like_count_tag.get_text()
        print(f"Likes: {like_count}")

    # 3. 해시태그 추출 (해시태그는 #이 앞에 붙은 글자)
    hashtags = []
    for tag in post_list_body.find_all('a', href=True):  # 해시태그가 a 태그에 있는 경우로 가정
        if tag.get_text().startswith('#'):
            hashtags.append(tag.get_text())

    print(f"Hashtags: {', '.join(hashtags)}")

    # 5. 작성자 추출 (class="nick" 내부 텍스트)
    author_tag = post_list_body.find('span', class_='nick')
    if author_tag:
        author = author_tag.get_text()
        print(f"Author: {author}")

    # 6. 본문 텍스트 추출
    main_container = post_list_body.find('div', class_='se-main-container')
    """ if main_container:
        content_text = main_container.get_text(strip=True)
        print(f"Content: {content_text}") """
    if main_container:
        span_tags = main_container.find_all('span')
        for span in span_tags:
            content_text = span.get_text(strip=True)
            print(content_text)


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

    # 디렉토리가 없으면 생성
    if not os.path.exists('html'):
        os.makedirs('html')

    save_path = os.path.join('html', 'playwright_naver.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    title = await page.title()

    # : 뒤의 내용 제거
    cleaned_title = title.split(':')[0]
    print(f"Page title: {cleaned_title}")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())