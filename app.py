
import os
from flask import Flask, current_app
from threading import Thread
from views.utils import  init_redis
from views.index import index_bp
from views.redirect import redirect_bp
from views.stats import stats_bp
from views.log_writer import redis_listener

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "MY_SECRET_KEY")

@app.before_first_request
def before_first_request():
    current_app.redis = init_redis()
    Thread(target=redis_listener, args=(app, current_app.redis)).start()


app.register_blueprint(index_bp)
app.register_blueprint(redirect_bp)
app.register_blueprint(stats_bp)

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", False))