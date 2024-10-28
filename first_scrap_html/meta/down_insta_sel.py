import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run():
    target_url = 'https://www.instagram.com/p/DAIYj4CyoZv/'  # 로그인 후 접근할 페이지
    file_name = 'instagram_selenium.html'

    # Chrome WebDriver 설정 (headless=True로 설정하면 브라우저가 보이지 않음)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # 브라우저 최대화
    chrome_options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
    service = Service(executable_path='path/to/chromedriver')  # chromedriver 경로 지정

    # 브라우저 실행
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 페이지로 이동
    driver.get(target_url)

    # 페이지 로딩을 기다림
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("페이지 로딩 완료")
    except Exception as e:
        print(f"페이지 로딩 실패: {e}")
        driver.quit()
        return

    # 페이지 새로고침
    time.sleep(3)
    driver.refresh()
    time.sleep(3)

    # HTML 내용 가져오기
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # 모든 <script> 요소 제거
    for script in soup.find_all('script'):
        script.decompose()

    # 클래스가 "xoegz02"인 모든 <div> 제거
    for div in soup.body.find_all('div', class_='xoegz02'):
        div.decompose()

    # HTML 파일로 저장
    save_path = os.path.join('html', file_name)
    os.makedirs('html', exist_ok=True)  # 폴더가 없으면 생성
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(f"HTML 소스가 '{file_name}'에 저장되었습니다.")

    # 스크린샷 찍기
    driver.save_screenshot("instagram_screenshot.png")

    # 브라우저 종료
    driver.quit()

if __name__ == "__main__":
    run()
