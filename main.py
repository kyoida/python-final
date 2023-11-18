from flask import Flask, render_template, request, session, redirect, url_for
from database.models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///savoir.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'NCT127DREAMWAYV'

db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(login=login, password=password).first()

        if user:

            session['user_id'] = user.user_id
            session['username'] = user.login
            return redirect(url_for("index"))
        else:
            return render_template("login.html", context="Invalid credentials. Please try again.")

    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form['username']
        fname = request.form['fname']
        sname = request.form['sname']
        pass1 = request.form['password']


        existing_user = User.query.filter_by(login=login).first()

        if existing_user:
            return render_template("registration.html", context="Username is already taken.")

        else:
            new_user = User(login=login, user_fname=fname, user_sname=sname, password=pass1)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login", context="Successfully registered!"))

    return render_template("registration.html")


if __name__ == "__main__":
    with app.app_context():  # Ensuring the code runs within the application context
        db.create_all()  # Creating the database tables
    app.run(debug=True)