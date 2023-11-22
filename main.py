from flask import Flask, render_template, request, session, redirect, url_for
from database.models import db, User, CartItem, Product

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

        user = User.query.filter_by(login=login, password=password).first()

        if user:

            session['user_id'] = user.user_id
            session['username'] = user.login
            return redirect(url_for("account"))
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
        cart_item = CartItem.query.filter_by(product_name=product.name, user_id=user_id).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            new_cart_item = CartItem(
                product_name=product.name,
                quantity=1,
                price=product.price,
                user_id=user_id
            )
            db.session.add(new_cart_item)

        db.session.commit()

    return redirect(url_for('view_products'))


@app.route('/remove_from_cart/<int:product_id>', methods=["POST", "GET"])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    product = get_product_by_id(product_id)

    if product:
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
        products = Product.query.all()
        print("Products:", products) 
        return render_template('products.html', products=products)
    except Exception as e:
        print(f"Error fetching products: {e}")
        return "Internal Server Error", 500


@app.route('/add_watch', methods=["POST", "GET"])
def add_watch():
    if 'username' in session and session['username'] == 'Admin':
        products = Product.query.all()

        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price', 0.0))  
            img_url = request.form.get('img_url')

            new_product = Product(name=name, description=description, price=price, img_url=img_url)
            db.session.add(new_product)
            db.session.commit()

            return redirect(url_for('add_watch'))

        elif request.method == "GET":
            return render_template('add_watch.html', products=products)

    return "Unauthorized access"


@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user is None:
        return "User not found", 404
    return render_template('account.html', user=user)


@app.route('/mechanism')
def show_mechanism():
    return render_template('mechanism.html')


@app.route('/giftcard')
def giftcard():
    return render_template('giftcard.html')

@app.route('/about_company')
def about_company():
    return render_template('about_company.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('login', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)