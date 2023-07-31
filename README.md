# Python으로 스크래핑


- 파이썬 스크립트 실행
```
$ python main.py
```

- 파이썬 패키지 관리 - pip 설치
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
```
$ sudo apt install python3.10-venv

$ python3 -m venv [가상환경 이름]
```
가상환경 활성화
```
$ source [가상환경 이름]/bin/activate
```
## poetry
```
$ curl -sSL https://install.python-poetry.org | python -

$ poetry new [프로젝트명]
```
가상 환경 실행
```
$ poetry run python main.py
```

---

<br>


## beautifulsoup4
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

```
$ poetry add flask
```
- 기본 구조
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
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