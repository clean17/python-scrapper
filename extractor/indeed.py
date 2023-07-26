from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup

# browser_channel = ['chromium', 'firefox', 'webkit'] # 워크플로우에서 사용할 경우
# for channel in browser_channel:
#     os.system(f"python -m playwright install {channel} --with-deps")

def extract_indeed_job(keyword):
    base_url = "https://kr.indeed.com/jobs?q="
    results = []

    def run(playwright: Playwright):
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537')
        page = context.new_page()
        page.goto(f"{base_url}{keyword}")

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
                        'company': company,
                        'location': location,
                        'position': title,
                    }
                    results.append(job_data)
        # for result in results:
        #     print(result, '\n')
        context.close()
        browser.close()

    with sync_playwright() as playwright: # with를 사용하면 컨텍스트 관리자가 자동으로 종료
        run(playwright)
        
    return results;