from flask import Flask
from database.models import db  # Import the db instance

app = Flask(__name__)

# Adding database URI to a config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Desktop/final/instance/savoir.db'
app.config['SECRET_KEY'] = "NCT127DREAMWAYV"

# Initialize SQLAlchemy with the Flask app
db.init_app(app)
