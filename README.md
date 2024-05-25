# Python 스크래핑


- 파이썬 스크립트 실행 명령어
```
$ python main.py
```

- 파이썬 패키지 관리를 위한 pip 패키지 설치
```
$ touch get-pip.py
```
`https://bootstrap.pypa.io/get-pip.py` 내용 복사 후 실행
```
$ python get-pip.py
```
---
<br>

> 가상 환경으로 파이썬 관리
## venv
파이썬의 표준 라이브러리<br>
프로젝트마다 독립된 가상 환경을 제공하여 의존성 충돌을 방지

아래 명령어로 설치되어 있는 3.10버전 파이썬에 가상환경을 추가
```
$ sudo apt install python3.10-venv

$ python3 -m venv [가상환경 이름]
```
가상환경 활성화 (리눅스/윈도우)
```
$ source [가상환경 이름]/bin/activate

$ [가상환경 이름]\Scripts\activate
```
가상환경 비활성화
```
$ deactivate
```

## poetry
poetry는 파이썬의 패키지 관리와 의존성 관리를 간편하게 하도록 도와주는 도구<br>
가상환경 관리뿐만 아니라(venv) 패키지 설치, 프로젝트 설정, 빌드, 배포까지 포괄적인 기능을 제공
```
$ curl -sSL https://install.python-poetry.org | python -

$ poetry new [프로젝트명]
```
새로운 프로젝트를 만들면 `[프로젝트명]` 의 디렉토리가 만들어지고 기본적인 파일구조와 `pyproject.toml`를 생성한다

프로젝트에 의존성 추가 명령어 -> `pyproject.toml` 파일에 반영된다
```
$ poetry add requests 
```
가상 환경 활성화
```
$ poetry shell
```
가상 환경의 프로젝트 실행
```
$ poetry run python main.py
```
패키지 배포
```
$ poetry build
$ poetry publish

```

요약 <br>

간단한 가상환경 구축 - venv <br>
가상환경 + 의존성 + 배포 - poetry

---

<br>


## beautifulsoup4
파이썬에서 `html`, `xml` 을 파싱해 추출해주는 라이브러리


- f-string 사용 방법
```py
name = "Alice"
age = 30
formatted_string = f"Hello, my name is {name} and I am {age} years old."
print(formatted_string)

# Hello, my name is Alice and I am 30 years old.

name = "Charlie"
age = 25
bio = f"""
Name: {name}
Age: {age}
"""
print(bio)

# Name: Charlie
# Age: 25
```

- 간단한 사용 예
```py
from bs4 import BeautifulSoup
import requests

# 웹 페이지 요청
url = 'http://example.com'
response = requests.get(url)

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 특정 태그 찾기 (예: 모든 <a> 태그)
links = soup.find_all('a')

# 링크 출력
for link in links:
    print(link.get('href'))

```


- 스크래핑 + f-string

```python
from requests import get

res = get(f'{base_url}{serach_term}')
```

## Playwright
- 브라우저 자동화 라이브러리
```
$ poetry add playwright
```
playwright 브라우저 설치
```
$ python -m playwright install

```
- 스크래핑 코드
```python
def extract_indeed_job(keyword):
    pages = get_page_count(keyword)
    results = [] 
    print(f'Found {pages} pages')
    for pageNum in range(pages):
        base_url = "https://kr.indeed.com/jobs?q="
        def run(playwright: Playwright):
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537')
            page = context.new_page()
            pagenation = pageNum * 10
            page.goto(f"{base_url}{keyword}&start={pagenation}", timeout=60000)
            print(f"{base_url}{keyword}&start={pagenation}",'\n')

            soup = BeautifulSoup(page.content(), "html.parser")
            job_list = (soup.find("ul", class_="jobsearch-ResultsList"))
            jobs = job_list.find_all('li', recursive=False)
            
            for job in jobs:
                zone = job.find('div', class_='mosaic_zone')
                if zone == None: # null
                    anchor = job.select_one('h2 a')
                    if anchor != None:
                        title = anchor['aria-label']
                        link = anchor['href']
                        company = job.select_one('span.companyName').text
                        location = job.select_one('div.companyLocation').text
                        job_data = {
                            'link': f"https://kr.indeed.com{link}",
                            'company': company.replace(","," "),
                            'location': location.replace(","," "),
                            'position': title.replace(","," "),
                        }
                        results.append(job_data)
            context.close()
            browser.close()

        with sync_playwright() as playwright: # with를 사용하면 컨텍스트 관리자가 자동으로 종료
            run(playwright)
        
    return results   
```

---

<br>

## Flask
마이크로 웹 프레임워크
```
$ poetry add flask
```
- 기본 구조
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/sum', methods=['POST'])
def sum_numbers():
    data = request.get_json()
    total = sum(data['numbers'])
    return jsonify({'total': total})

if __name__ == '__main__':
    app.run(debug=True)

```

## Jinja2 - 템플릿 엔진
- 동적인 SSR 반환 `{{ }}`
```python
render_template('home.html', name = "merci")

->  {{name}}
```
- 쿼리스트링 접근
```python
request.args.get('keyword', '')
```

- 템플릿 제어 구조 `{% %}`
```html
    {% for job in jobs  %}
        <div>{{job.link}}</div>
    {% endfor %}
```

- 파일 저장 코드
```python
from flask import Flask, render_template, request, redirect, send_file
from extractor.indeed import extract_indeed_job
from extractor.wwr import extractor_wwr_jobs
from file import save_to_file

app = Flask(__name__)

db = {}

@app.route('/')
def hello_world():
    return render_template('home.html', name = "merci")


@app.route('/search')
def serach():
    keyword = request.args.get('keyword')
    if keyword == None:
        return redirect('/')
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_indeed_job(keyword)
        wwr = extractor_wwr_jobs(keyword)
        jobs = indeed + wwr
        db[keyword] = jobs
    return render_template('search.html', keyword = keyword, jobs = jobs)

@app.route('/export')
def export():
    keyword = request.args.get('keyword')
    if keyword == None:
        return redirect('/')
    elif keyword not in db:
        return  redirect(f'/serach?keyword={keyword}')
    save_to_file(keyword, db[keyword])
    return send_file(f'{keyword}.csv', as_attachment=True)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
```




### 블로그 정리
https://velog.io/@merci/python-%EC%8A%A4%ED%81%AC%EB%9E%98%ED%8D%BC <br><br>