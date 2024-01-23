import json 
from .utils import get_db_conn, init_redis
from redis import Redis
from flask import Flask, current_app, appcontext_pushed, appcontext_popped


def redis_listener():
    def handle_request(_):
        # 當進入上下文時執行的代碼
        current_app.redis = init_redis()

    def handle_teardown(_):
        # 當離開上下文時執行的代碼
        pass

    with appcontext_pushed(current_app):
        # 進入上下文
        appcontext_pushed.connect(handle_request, current_app._app)

        # 處理相關邏輯
        try:
            # 在這裡使用 current_app 訪問 Flask 應用程式的其他設定
            redis_conn = current_app.redis
            while True:
                try:
                    _, click_data_str = redis_conn.brpop('url_visits', timeout=0)
                    
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
    
        except Exception as e:
            print(f"Error in redis_listener: {e}")
        finally:
            appcontext_popped.connect(handle_teardown, current_app._app)
