import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# JSESSIONID 설정
JSESSIONID = 'oVL1NLairN6qkI2NQN0j6Dr4MPu9uDb4o5T7OUZB15vkIZsIvQUKsW4Gvwuccc3U.amV1c19kb21haW4vbGFyaXNfc2VydmVy'

# 브라우저 드라이버 설정 (헤드리스 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저를 안 열리게 함
chrome_options.add_argument("--disable-gpu")  # 일부 시스템에서 발생할 수 있는 GPU 관련 문제 방지
chrome_options.add_argument("--window-size=1920x1080")  # 브라우저 해상도 설정 (필요시 조정)

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

# 페이지 열기 (먼저 로그인 세션 쿠키를 설정하기 전에 기본 URL 열기)
driver.get('http://192.168.60.101:8080')

# JSESSIONID 쿠키 추가
driver.add_cookie({
    'name': 'JSESSIONID',
    'value': JSESSIONID,
    'domain': '192.168.60.101',  # 도메인 맞추기
    'path': '/'
})

# 필요한 페이지로 이동
driver.get('http://192.168.60.101:8080/archives/regArchivesDoc/viewFolderReg/view?modeType=edit-folder-mode&title=%EA%B8%B0%EB%A1%9D%EB%AC%BC+%EC%B2%A0+%EB%93%B1%EB%A1%9D&type=edit-folder-mode&tsiFolderKind=RKD-1-1&tsiFolderStts=WRK-4-1&tsiFolderRole=')

# 첫 번째 input 요소 찾기 (UUIDKey)
try:
    uuid_key_element = driver.find_element(By.XPATH, '//input[@name="UUIDKey"]')
    uuid_key_value = uuid_key_element.get_attribute('value')

    # 두 번째 input 요소 찾기 (UUIDKey 값으로 찾기)
    uuid_value_element = driver.find_element(By.XPATH, f'//input[@name="{uuid_key_value}"]')
    uuid_value = uuid_value_element.get_attribute('value')

    # 환경 변수 설정 (Windows 기준, Linux/Mac은 별도 설정 필요)
    os.system(f'setx UUIDKey "{uuid_key_value}"')
    os.system(f'setx "{uuid_key_value}" "{uuid_value}"')

    # 확인을 위해 출력
    print(f'UUIDKey: {uuid_key_value}')
    print(f'{uuid_key_value}: {uuid_value}')

    # 절대 경로로 파일 저장하기
    file_path = r"C:\Users\user\Downloads\apache-jmeter-5.6.2\apache-jmeter-5.6.2\uuid_values.txt"

    with open(file_path, "w") as file:
        file.write(f"{uuid_value}\n")


except Exception as e:
    print(f"오류 발생: {e}")

# 브라우저 닫기
driver.quit()
