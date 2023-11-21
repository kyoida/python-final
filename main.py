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

    # Pass cart_items to the render_template function
    return render_template('cart.html', cart_items=cart_items)


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
                quantity=1,
                price=product.price,
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
    try:
        # Retrieve all products from the database
        products = Product.query.all()
        print("Products:", products)  # Add this print statement
        return render_template('products.html', products=products)
    except Exception as e:
        # Print or log the exception for debugging
        print(f"Error fetching products: {e}")
        return "Internal Server Error", 500


@app.route('/add_watch', methods=["POST", "GET"])
def add_watch():
    # Check if the user is logged in and is an admin
    if 'username' in session and session['username'] == 'Admin':
        products = Product.query.all()

        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price', 0.0))  # Assuming the price is a float
            img_url = request.form.get('img_url')

            new_product = Product(name=name, description=description, price=price, img_url=img_url)
            db.session.add(new_product)
            db.session.commit()

            # Redirect to the add_watch page after the POST request to avoid form resubmission on page refresh
            return redirect(url_for('add_watch'))

        elif request.method == "GET":
            # Handle the GET request as needed
            return render_template('add_watch.html', products=products)

    # If the user is not an admin or not logged in, you can redirect or display an error message.
    return "Unauthorized access"


@app.route('/watches')
def show_watches():
    watches = Product.query.all()
    return render_template('watches.html', watches=watches)


@app.route('/mechanism')
def show_mechanism():
    return render_template('mechanism.html')


@app.route('/giftcard')
def giftcard():
    return render_template('giftcard.html')


@app.route('/logout')
def logout():
    # Clear the user-related session variables
    session.pop('user_id', None)
    session.pop('login', None)

    # Redirect to the login page or any other desired destination
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context(): # Ensuring the code runs within the application context
        db.create_all()  # Creating the database tables
    app.run(debug=True)