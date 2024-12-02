from flask import Flask

# imports views, creates a Flask app, registers the blueprint, and returns the app object
def startServer(**kwargs):
    from .views import views
    from .reports import reports
    from .auth import auth
    
    app = Flask(__name__)

    for key, value in kwargs.items():
        app.config[key] = value

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(reports, url_prefix='/reports/')
    app.register_blueprint(auth, url_prefix='/auth/')
    return app