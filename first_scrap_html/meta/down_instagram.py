import asyncio
import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def run(playwright):
    target_url = 'https://www.instagram.com/p/DAIYj4CyoZv/'  # 로그인 후 접근할 페이지
    file_name = 'instagram_playwright.html'

    # 브라우저 실행 (headless=False로 설정하면 브라우저가 보임)
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

    # 로그인 후 특정 페이지로 이동
    await page.goto(target_url)
    await page.wait_for_timeout(3000)  # 페이지 로딩 대기
    await page.reload()
    await page.wait_for_timeout(3000)  # 페이지 로딩 대기

    # 페이지의 HTML 내용 가져오기
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # 모든 <script> 요소 제거
    for script in soup.find_all('script'):
        script.decompose()  # 메모리에서 완전 삭제

    # 모든 div 요소 중 클래스가 "xoegz02"인 것 제거
    for div in soup.body.find_all('div', class_='xoegz02'):
        div.decompose()


    # body = soup.body
    # await asyncio.sleep(2)
    # top_level_divs = body.find_all('div', recursive=False)
    # if top_level_divs:
    #     top_level_divs[-1].decompose() # decompose 메모리에서 완전 삭제, extract 트리에서만 삭제 반환 가능

    # HTML 파일로 저장
    save_path = os.path.join('html', file_name)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # 스크린샷 찍기
    # await page.screenshot(path="instagram_screenshot.png", full_page=True)

    print(f"HTML 소스가 '{file_name}'에 저장되었습니다.")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main()) # 비동기 이벤트 루프 시작
