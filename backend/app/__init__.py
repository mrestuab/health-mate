from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import threading
import schedule
import time
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*") 

from app import routes


# from app.model import user, medicine, reminder, notification


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

# socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, debug=True) 
