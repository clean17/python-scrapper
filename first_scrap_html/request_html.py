import requests
from bs4 import BeautifulSoup

def save_html_source(url, file_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
    except Exception as e:
        print("Error: ", e)


'''
다음은 되지만 네이버는 안된다.. 동적인 요청이 필요하다
'''
if __name__ == "__main__":
#     url = 'https://www.daum.net'
    url = 'https://www.naver.com'
#     save_html_source(url, 'daum.html')
    save_html_source(url, 'naver.html')
