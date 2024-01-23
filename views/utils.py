from flask import current_app
from redis import Redis
from hashids import Hashids
import sqlite3
from datetime import datetime, timedelta
from collections import Counter

def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_hashids():
    return Hashids(min_length=4, salt=current_app.config['SECRET_KEY'])

def init_redis():
    return Redis(host='redis', port=6379, decode_responses=True)

def get_nearest_days_data(data, days = 10):
    dates = [datetime.strptime(entry['created'], '%Y-%m-%d %H:%M:%S').date() for entry in data]
    latest_date = datetime.now().date()
    date_labels = [(latest_date - timedelta(days=i)).strftime('%Y/%m/%d') for i in range(days, -1, -1)]
    date_counts = Counter(dates)
    counts = [date_counts.get(datetime.strptime(label, '%Y/%m/%d').date(), 0) for label in date_labels]
    return counts, date_labels