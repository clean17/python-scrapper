from requests import get
from bs4 import BeautifulSoup
from extractor.wwr import extractor_wwr_jobs

jobs = extractor_wwr_jobs('python');
print(jobs)