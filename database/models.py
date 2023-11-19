from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    user_fname = db.Column(db.String(255))
    user_sname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)

class CartItem(db.Model):
    __tablename__ = "cart_items"
    item_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)



