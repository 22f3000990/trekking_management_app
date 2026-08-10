from flask import Flask
from config import Config
from models.models import db, User
from flask_login import LoginManager
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from routes.trekker_routes import trekker_bp
from flask_cors import CORS
import redis
from celery_app import make_celery
from tasks import register_tasks

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    redis_client = redis.from_url(app.config['REDIS_URL'])
    app.redis_client = redis_client
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)

    app.register_blueprint(admin_bp)

    app.register_blueprint(staff_bp)

    app.register_blueprint(trekker_bp)

    celery = make_celery(app)
    app.celery = celery
    app.export_task, app.report_task = register_tasks(celery, app)

    return app

flask_app = create_app()
celery = flask_app.celery

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)