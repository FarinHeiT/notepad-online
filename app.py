from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

# The app can be launched through "flask run" or 
# directrly through running "main.py"

app = Flask(__name__)
app.config.from_object(Config)

# database object
db = SQLAlchemy(app)

# migration object
migrate = Migrate(app, db)

# login object
login_manager = LoginManager()
login_manager.init_app(app)

# We load views and blueprints here because of circular imports  
from auth.auth_bp import auth
import view
app.register_blueprint(auth, url_prefix='/auth')
