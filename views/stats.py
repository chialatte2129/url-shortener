from flask import Blueprint, render_template, request, flash, redirect, url_for
from .utils import get_db_conn, init_hashids, get_nearest_days_data
from datetime import datetime, timedelta

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats')
def stats():
    conn = get_db_conn()
    db_urls = conn.execute('SELECT id, created, original_url FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['created'] = datetime.strptime(url['created'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        url['url_id'] = init_hashids().encode(url['id'])
        url['short_url'] = request.host_url + url['url_id']
        urls.append(url)
    return render_template('stats.html', urls=urls)



@stats_bp.route('/stats/<string:id>')
def id_stats(id):
    original_id = init_hashids().decode(id)[0]
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