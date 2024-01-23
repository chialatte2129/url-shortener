from flask import Blueprint, redirect, flash, url_for, request, current_app
from .utils import get_db_conn, init_hashids
from datetime import datetime, timedelta
import json

redirect_bp = Blueprint('redirect', __name__)

@redirect_bp.route('/<string:id>')
def url_redirect(id):
    if current_app.redis.exists(id):
        original_url = current_app.redis.get(id)
    else:
        conn = get_db_conn()
        original_id = init_hashids().decode(id)
        if original_id:
            original_id = original_id[0]
            url_data = conn.execute(f"SELECT original_url FROM urls WHERE id = ({original_id})").fetchone()
            original_url = url_data['original_url']
            current_app.redis.set(id, original_url)
            conn.close()
        else:
            flash('Invalid URL')
            return redirect(url_for('index.index'))
        
    # send id to redis queue
    push_data = {
        "id":init_hashids().decode(id)[0],
        "ip_address":request.remote_addr,
        "user_agent":request.user_agent.string,
        "created":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    current_app.redis.rpush('url_visits', json.dumps(push_data))
    return redirect(original_url)