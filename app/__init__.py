import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'devkey')

    db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if db_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    else:
        server = os.getenv("SQL_SERVER", "MAHSRV")
        database = os.getenv("SQL_DATABASE", "factorydb")
        user = os.getenv("SQL_USER", "sa")
        password = os.getenv("SQL_PASSWORD", "")
        odbc_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}"
        app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={odbc_str}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    login_manager.init_app(app)

    from .models import User  # noqa

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("403.html"), 403

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    # Logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

    # Register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
