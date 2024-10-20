import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import configparser

config = configparser.ConfigParser()

config.read('config.ini')

UESRNAME = config['INSTAGRAM']['UESRNAME']
PASSWORD = config['INSTAGRAM']['PASSWORD']

async def run(playwright):
    # 인스타그램 로그인 페이지
        login_url = 'https://www.instagram.com/accounts/login/'
        target_url = 'https://www.instagram.com/p/DAIYj4CyoZv/'  # 로그인 후 접근할 페이지
        file_name = 'instagram_playwright.html'

        # Instagram 계정 정보
        instagram_username = UESRNAME
        instagram_password = PASSWORD

        # 브라우저 실행 (headless=False로 설정하면 브라우저가 보임)
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        '''
        # 로그인 페이지로 이동
        await page.goto(login_url)
        await page.wait_for_timeout(2000)  # 페이지 로딩 대기

        # 로그인 폼에 아이디와 비밀번호 입력
        await page.fill('input[name="username"]', instagram_username)
        await page.fill('input[name="password"]', instagram_password)

        # 로그인 버튼 클릭
        await page.click('button[type="submit"]')

        # 로그인 후 페이지 로딩 대기 (2단계 인증 등 다른 팝업이 있을 수 있으므로 wait_for_navigation 사용 가능)
        await page.wait_for_timeout(5000)  # 로그인 과정 대기
        '''

        # 로그인 후 특정 페이지로 이동
        await page.goto(target_url)
        await page.wait_for_timeout(3000)  # 페이지 로딩 대기

        # 스크린샷 찍기
        await page.screenshot(path="instagram_screenshot.png", full_page=True)

        # 페이지의 HTML 내용 가져오기
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        body = soup.body
        await asyncio.sleep(2)

        # body 하위 직속 div 요소들 찾기
        top_level_divs = body.find_all('div', recursive=False)
        if top_level_divs:
            top_level_divs[-1].decompose() # decompose 메모리에서 완전 삭제, extract 트리에서만 삭제 반환 가능

        # HTML 파일로 저장
        save_path = os.path.join('html', file_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        print(f"HTML 소스가 '{file_name}'에 저장되었습니다.")
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main()) # 비동기 이벤트 루프 시작
