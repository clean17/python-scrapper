import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

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
    await page.goto('https://x.com/happymoj/status/1691995174367596841')
    #     await page.wait_for_load_state('networkidle')  # 네트워크 요청이 완전히 끝날 때까지 대기 - 스켈레톤으로 나온다

    await scroll_to_bottom(page)
    #     await page.screenshot(path="full_page_screenshot.png", full_page=True)

    content = await page.content()
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')

    # <script> 태그 모두 제거
    for script in soup.find_all('script'):
        script.decompose()  # 해당 태그와 내용을 제거

    # <article aria-labelledby="로 시작하는 모든 태그를 찾기
    articles = soup.find_all('article', {'aria-labelledby': True})

    if articles:
        # <body> 태그 찾기
        body_tag = soup.find('body')

        if body_tag:
            # <body> 태그 내부를 비우기
            body_tag.clear()

            # 찾은 모든 <article> 태그를 <body>에 추가
            for article in articles:
                body_tag.append(article)

            # 추가적인 스타일링을 위한 <style> 태그 추가
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
            soup.head.append(style_tag)  # <head>에 <style> 추가

    # 수정된 HTML을 파일로 저장
    with open('filtered_articles.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
        print(soup.prettify())

    title = await page.title()
    print(f"Page title: {title}")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())