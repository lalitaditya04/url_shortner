from flask import Flask, render_template
from config import Config
from app.extensions import mongo, bootstrap

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    bootstrap.init_app(app)

    from app.routes.api import api_bp
    from app.routes.views import views_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
