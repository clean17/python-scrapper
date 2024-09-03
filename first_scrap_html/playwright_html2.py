import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run(playwright):
    browser = await playwright.chromium.launch()
    # browser = await playwright.chromium.launch(headless=False)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()
    await page.goto('https://www.naver.com')

    # 주요 요소가 로드될 때까지 기다림 (예: 메인 콘텐츠나 특정 이미지가 로드될 때까지)
    await page.wait_for_selector('img')

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    with open('playwright_naver2.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    title = await page.title()
    print(f"Page title: {title}")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
