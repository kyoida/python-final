from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///savoir.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'NCT127DREAMWAYV'  # Set a secret key for session management
db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():  # Ensuring the code runs within the application context
        db.create_all()  # Creating the database tables
    app.run(debug=True)


    # dfhv