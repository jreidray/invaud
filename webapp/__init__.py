from flask import Flask

# imports views, creates a Flask app, registers the blueprint, and returns the app object
def startServer():
    from .views import views
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "invaud_key"
    app.register_blueprint(views, url_prefix='/')
    return app