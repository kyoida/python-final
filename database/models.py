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

    def __init__(self, login, user_fname, user_sname, password):
        self.login = login
        self.user_fname = user_fname
        self.user_sname = user_sname
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {"login": self.login,
                "user_fname": self.user_fname,
                "user_sname": self.user_sname
                }


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __init__(self, img_url, name, price, description):
        self.img_url = img_url
        self.name = name
        self.price = price
        self.description = description

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {"id": self.product_id,
                "name": self.name,
                "img_url": self.img_url,
                "description": self.description,
                "price": self.price}


class CartItem(db.Model):
    __tablename__ = "cart_items"
    item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, user_id, product_id, quantity=1):
        self.user_id = user_id
        self.mug_id = product_id
        self.quantity = quantity

    def update_quantity(self, quantity):
        self.quantity += quantity
        db.session.commit()

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()