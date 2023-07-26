from extractor.indeed import extract_indeed_job
from extractor.wwr import extractor_wwr_jobs

keyword = input('please input Language?  ')

wwr = extractor_wwr_jobs(keyword)
indeed = extract_indeed_job(keyword)
jobs = wwr + indeed

file = open(f"{keyword}.csv", "w")
file.write('Position, Company, Location, URL\n')

for job in jobs:
    file.write(f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n")
file.close()