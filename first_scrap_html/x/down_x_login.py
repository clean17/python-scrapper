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
    # X 웹사이트의 로그인 페이지와 타겟 페이지
    login_url = 'https://x.com/login'
    target_url = 'https://x.com/happymoj/status/1691995174367596841'
    file_name = 'test2_down_x.html'

    # X 계정 정보 (예시, 실제 로그인 정보 사용)
    x_username = "inu240920"
    x_password = "!Pass9900"

    # 브라우저 실행 (headless=False로 설정하면 브라우저가 보입니다)
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

    # 로그인 페이지로 이동
    await page.goto(login_url)
    await page.wait_for_timeout(2000)  # 페이지 로딩 대기

    # 로그인 폼에 아이디와 비밀번호 입력
    await page.fill('input[name="text"]', x_username)  # 아이디 입력
    await page.press('input[name="text"]', 'Enter')  # 아이디 입력 후 Enter 키 입력

    await page.wait_for_timeout(2000)  # 비밀번호 입력 폼 대기
    await page.fill('input[name="password"]', x_password)  # 비밀번호 입력
    await page.press('input[name="password"]', 'Enter')  # 비밀번호 입력 후 Enter 키 입력

    # 로그인 후 페이지 로딩 대기
    await page.wait_for_timeout(3000)

    # 타겟 페이지로 이동
    await page.goto(target_url)
    await page.wait_for_timeout(3000)

    # 페이지 끝까지 스크롤
    await scroll_to_bottom(page)

    # 페이지 HTML 가져오기
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # <script> 태그 모두 제거
    for script in soup.find_all('script'):
        script.decompose()

    # <article aria-labelledby="로 시작하는 모든 태그를 찾기
    articles = soup.find_all('article', {'aria-labelledby': True})

    if articles:
        body_tag = soup.find('body')
        if body_tag:
            body_tag.clear()
            for article in articles:
                body_tag.append(article)

            style_tag = soup.new_tag('style')
            style_tag.string = '''
            body {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100vh;
                margin: 0;
            }

            article {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
            }
            '''
            soup.head.append(style_tag)

    save_path = os.path.join('html', file_name)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    title = await page.title()
    print(f"Page title: {title}")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
