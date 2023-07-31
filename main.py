from flask import Flask, render_template, request
from extractor.indeed import extract_indeed_job
from extractor.wwr import extractor_wwr_jobs

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html', name = "merci")


@app.route('/search')
def serach():
    keyword = request.args.get('keyword', 'not keyword')
    indeed = extract_indeed_job(keyword)
    wwr = extractor_wwr_jobs(keyword)
    jobs = indeed + wwr
    return render_template('search.html', keyword = keyword, jobs = jobs)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
