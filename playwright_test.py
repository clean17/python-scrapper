import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    await page.goto('https://velog.io/')
    title = await page.title()
    print(f"Page title: {title}")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
