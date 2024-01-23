from flask import Blueprint, render_template, request, flash, redirect, url_for
import validators
from .utils import get_db_conn, init_hashids

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_conn()
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index.index'))
        if not validators.url(url):
            flash('Invalid URL')
            return redirect(url_for('index.index'))   
        url_data = conn.execute("INSERT INTO urls (original_url) VALUES (?)", (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = init_hashids().encode(url_id)
        short_url = request.host_url + hashid
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')