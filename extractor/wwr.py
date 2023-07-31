from requests import get
from bs4 import BeautifulSoup

def extractor_wwr_jobs(keyword):    
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
  results = []
  res = get(f'{base_url}{keyword}')
  if res.status_code != 200:
    print("request failed")
  else:
    html_doc = res.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    job_posts = soup.select('section.jobs li')
    # job_posts.pop(-1)
    for post in job_posts:
      anchors = post.find_all('a')
      if len(anchors) > 1:
        anchor = anchors[1]
        link = anchor['href']
        company, kind, region = anchor.find_all('span', class_='company')
        title = anchor.find('span', class_='title')
        job_data = {
          'link': f"https://weworkremotely.com{link}",
          'company': company.text.replace(","," "),
          'location': region.text.replace(","," "),
          'position': title.text.replace(","," "),
        }
        results.append(job_data)
    # for result in results:
    #   print(result)
    return results