import os
import zipfile
import shutil
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get

chrome_driver_version = "94.0.4606.41"
chrome_driver_url = f"https://chromedriver.storage.googleapis.com/{chrome_driver_version}/chromedriver_linux64.zip"

response = get(chrome_driver_url)
zip_file_path = "chromedriver.zip" # 다운 받은 파일 이름 지정
with open(zip_file_path, "wb") as f:
    f.write(response.content)

with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall()

chrome_driver_path = os.path.abspath("chromedriver") # 절대 경로 반환
os.chmod(chrome_driver_path, 0o755)

executable_path = os.path.join('/usr/local/bin', "chromedriver") # 경로 생성
# shutil.move(chrome_driver_path, executable_path) # 이동 , /usr/local/bin - 시스템 디렉토리, 권한 필요
os.remove(zip_file_path)
# os.chmod(executable_path, 0o755)

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")  # Linux 환경에서 root권한 실행 x
# chrome_options.add_argument("--disable-dev-shm-usage")  # Linux 환경에서 Chrome 실행시 /dev/shm 디렉토리 사용 x ( 메모리 제한 해제 )
# chrome_options.add_argument("--headless")  # Headless 모드 - 백그라운드 실행
# chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 (Headless 모드에서 필요)

# def get_page_count(keyword):
#     results = []
#     base_url = "https://kr.indeed.com/jobs?q="
#     driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)

    # service = webdriver.chrome.service.Service(executable_path="/usr/local/bin/chromedriver")
    # service.start()
    # driver = webdriver.Chrome(service=service, options=chrome_options)

    # driver.get(f"{base_url}{keyword}")

    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # job_list = (soup.find("ul", class_="jobsearch-ResultsList"))
    # jobs = job_list.find_all('li', recursive=False)
    
    # for job in jobs:
    #     zone = job.find('div', class_='mosaic_zone')
    #     if zone == None: # null
    #         anchor = job.select_one('h2 a')
    #         if anchor != None:
    #             title = anchor['aria-label']
    #             link = anchor['href']
    #             company = job.select_one('span.companyName').text
    #             location = job.select_one('div.companyLocation').text
    #             job_data = {
    #                 'link': f"https://kr.indeed.com{link}",
    #                 'company': company.replace(","," "),
    #                 'location': location.replace(","," "),
    #                 'position': title.replace(","," "),
    #             }
    #             results.append(job_data)
    # driver.quit()  # 브라우저를 종료합니다.
    # return results

# list = get_page_count("python")  
# print(list)

# os.environ["PATH"] += os.pathsep + os.path.abspath(os.path.dirname(executable_path))