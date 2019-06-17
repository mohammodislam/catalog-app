import os
from flask import Flask
import auth
import home
import category
import item
from db import db_session, init_db
from flask_json import FlaskJSON

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    FlaskJSON(app)
    app.secret_key = 'C3eROP6syUheoFpW66Om5IJu2EvUfOhR'
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')
    
    try:
      init_db()
    except:
      pass

    @app.teardown_appcontext
    def shutdown_session(exception=None):
      db_session.remove()
      
    return app