import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run(playwright):
    browser = await playwright.chromium.launch()
    # browser = await playwright.chromium.launch(headless=False)  # headless=False로 설정하면 브라우저가 보입니다.
    page = await browser.new_page()
    await page.goto('https://www.naver.com')
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
