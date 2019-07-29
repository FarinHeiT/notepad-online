from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate


# The app can be launched through "flask run" or 
# directrly through running "main.py"

app = Flask(__name__)
app.config.from_object(Config)

# database object
db = SQLAlchemy(app)

# migration object
migrate = Migrate(app, db)


# We load views and blueprints here because of circular imports  
from auth.auth_bp import auth
from text_entries.text_entries import textEntries
import view
app.register_blueprint(auth, url_prefix='/auth')
# No prefix for textEntries, but I created separate blueprint to keep things nice
app.register_blueprint(textEntries)
