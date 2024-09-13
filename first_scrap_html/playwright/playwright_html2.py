import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run(playwright):
    url = 'https://www.naver.com'
    file_name = 'playwright_naver2.html'

    browser = await playwright.chromium.launch()
    # browser = await playwright.chromium.launch(headless=False)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()
    await page.goto(url)

    # 주요 요소가 로드될 때까지 기다림 (예: 메인 콘텐츠나 특정 이미지가 로드될 때까지)
    await page.wait_for_selector('img')

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    title = await page.title()
    print(f"HTML 소스가 '{file_name}'에 저장되었습니다.")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main()) # 비동기 이벤트 루프 시작