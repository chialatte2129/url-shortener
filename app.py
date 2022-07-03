from redis import Redis
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this should be a secret random string'
redis = Redis(host='redis', port=6379, decode_responses=True)
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_conn()
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        if not validators.url(url):
            flash('Invalid URL')
            return redirect(url_for('index'))   
        url_data = conn.execute(f'INSERT INTO urls (original_url) VALUES ("{url}")')
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<string:id>')
def url_redirect(id):
    if redis.exists(id):
        original_url = redis.get(id)
    else:
        conn = get_db_conn()
        original_id = hashids.decode(id)
        if original_id:
            original_id = original_id[0]
            url_data = conn.execute(f"SELECT original_url FROM urls WHERE id = ({original_id})").fetchone()
            original_url = url_data['original_url']
            redis.set(id, original_url)
            conn.close()
        else:
            flash('Invalid URL')
            return redirect(url_for('index'))
    return redirect(original_url)

@app.route('/stats')
def stats():
    conn = get_db_conn()
    db_urls = conn.execute('SELECT id, created, original_url FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)

    return render_template('stats.html', urls=urls)

if __name__ == "__main__":
    app.run(debug=True)