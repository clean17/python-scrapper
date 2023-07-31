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