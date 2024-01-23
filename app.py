from redis import Redis
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import validators
import json
import os
import threading
from datetime import datetime, timedelta
from collections import Counter

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "MY_SECRET_KEY")
redis = Redis(host='redis', port=6379, decode_responses=True)
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

def redis_listener():
    while True:
        try:
            _, click_data_str = redis.brpop('url_visits', timeout=0)
            
            if click_data_str is not None:
                click_data = json.loads(click_data_str)
                id = click_data['id']
                ip_address = click_data['ip_address']
                user_agent = click_data['user_agent']
                created = click_data['created']
                
                conn = get_db_conn()
                conn.execute(f"INSERT INTO url_visits (url_id, ip_address, user_agent, created) VALUES ('{id}', '{ip_address}', '{user_agent}', '{created}')")
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"Error in redis_listener: {e}")

t = threading.Thread(target=redis_listener)
t.start()

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
        
    # send id to redis queue
    push_data = {
        "id":hashids.decode(id)[0],
        "ip_address":request.remote_addr,
        "user_agent":request.user_agent.string,
        "created":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    redis.rpush('url_visits', json.dumps(push_data))
    return redirect(original_url)

@app.route('/stats')
def stats():
    conn = get_db_conn()
    db_urls = conn.execute('SELECT id, created, original_url FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['created'] = datetime.strptime(url['created'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        url['url_id'] = hashids.encode(url['id'])
        url['short_url'] = request.host_url + url['url_id']
        urls.append(url)
    return render_template('stats.html', urls=urls)

def get_nearest_days_data(data, days = 10):
    dates = [datetime.strptime(entry['created'], '%Y-%m-%d %H:%M:%S').date() for entry in data]
    latest_date = datetime.now().date()
    date_labels = [(latest_date - timedelta(days=i)).strftime('%Y/%m/%d') for i in range(days, -1, -1)]
    date_counts = Counter(dates)
    counts = [date_counts.get(datetime.strptime(label, '%Y/%m/%d').date(), 0) for label in date_labels]
    return counts, date_labels

@app.route('/stats/<string:id>')
def id_stats(id):
    original_id = hashids.decode(id)[0]
    conn = get_db_conn()
    visit_data_exec = conn.execute(f"SELECT id, ip_address, created FROM url_visits WHERE url_id = ({original_id})").fetchall()
    target_url_result = conn.execute(f"SELECT original_url, created FROM urls WHERE id = ({original_id})").fetchone()
    url_data = {
        "target":target_url_result['original_url'],
        "from":request.host_url + id,
        "created":datetime.strptime(target_url_result['created'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d'),
    }
    conn.close()
    
    visit_data = []
    for row in visit_data_exec:
        row = dict(row)
        visit_data.append(row)
    url_data["total_visits"] = len(visit_data)
    values, labels = get_nearest_days_data(visit_data)
    visits = {"values":values, "labels":labels}

    return render_template('analyze.html', visits=visits, url_data=url_data)

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", False))