from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def save_html_source(url, file_name):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # GUI 없이 실행
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install()) # os 에 설치된 크롬 사용
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)

        # 페이지가 완전히 로드될 때까지 기다림
        time.sleep(5)  # 필요에 따라 조정

        html_source = driver.page_source

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(html_source)

        print(f"HTML 소스가 '{file_name}'에 저장되었습니다.")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    url = 'https://www.naver.com'
    file_name = 'selenium_naver.html'
    save_html_source(url, file_name)
