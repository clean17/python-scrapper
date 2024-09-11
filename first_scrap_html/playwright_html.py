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
                }, 50);
            });
        }
    """)

async def run(playwright):
#     browser = await playwright.chromium.launch()
    browser = await playwright.chromium.launch(headless=False)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()
    await page.goto('https://blog.naver.com/PostView.naver?blogId=mojjustice&logNo=223456814936')
#     await page.wait_for_load_state('networkidle')  # 네트워크 요청이 완전히 끝날 때까지 대기

    await scroll_to_bottom(page)

    content = await page.content()
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')
    with open('playwright_naver.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    title = await page.title()
    print(f"Page title: {title}")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
