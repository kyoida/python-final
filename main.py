from flask import Flask, render_template, request, session, redirect, url_for
from database.models import db, User, CartItem, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///savoir.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'NCT127DREAMWAYV'

db.init_app(app)


@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


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


@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    products = []
    final_total = 0
    for item in cart_items:
        product = Product.query.get(item.mug_id)
        product.quantity = item.quantity
        final_total += product.price * product.quantity
        products.append(product)

    return render_template('cart.html', product=product, final_total = final_total)


def get_product_by_id(product_id):
    return Product.query.get(product_id)


@app.route('/add_to_cart/<int:product_id>', methods=["POST", "GET"])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    product = get_product_by_id(product_id)

    if product:
        # Check if the item is already in the cart
        cart_item = CartItem.query.filter_by(product_name=product.name, user_id=user_id).first()

        if cart_item:
            # If item exists, update quantity
            cart_item.quantity += 1
        else:
            # If item does not exist, add it to the cart
            new_cart_item = CartItem(
                product_name=product.name,
                price=product.price,
                quantity=1,
                user_id=user_id
            )
            db.session.add(new_cart_item)

        db.session.commit()

    return redirect(url_for('index'))


@app.route('/remove_from_cart/<int:product_id>', methods=["POST", "GET"])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    product = get_product_by_id(product_id)

    if product:
        # Check if the item is already in the cart
        cart_item = CartItem.query.filter_by(product_name=product.name, user_id=user_id).first()

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.saveToDB()
        else:
            cart_item.deleteFromDB()

    return redirect(url_for('index'))


@app.route('/products')
def view_products():
    # Retrieve all products from the database
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])  # Assuming the price is a float

        new_product = Product(name=name, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('view_products'))


@app.route("/addmugs", methods=["POST", "GET"])
def addMug():
    # Assuming you have a 'username' variable in your session
    if 'username' in session:
        if session['login'] == 'Admin':
            product = Product.query.all()

            if request.method == "POST":
                name = request.form.get('title')
                img_url = request.form.get('img_url')
                description = request.form.get('description')
                price = request.form.get('price')

                product = Product(name=name, img_url=img_url, description=description, price=price)
                product.saveToDB()

                return render_template('add_watch.html', product=product)

            elif request.method == "GET":
                return render_template('add_watch.html', product=product)


@app.route('/watches')
def show_watches():
    watches = Product.query.all()
    return render_template('watches.html', watches = watches)


@app.route('/mechanism')
def show_mechanism():
    return render_template('mechanism.html')


@app.route('/giftcard')
def giftcard():
    return render_template('giftcard.html')


if __name__ == "__main__":
    with app.app_context():  # Ensuring the code runs within the application context
        db.create_all()  # Creating the database tables
    app.run(debug=True)