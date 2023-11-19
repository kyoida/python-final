from flaskapp import app
from database.models import db, Product


with app.app_context():
    watches = [
    Product(name="Classic Watch", price=250.0),
    Product(name="Modern Watch", price=300.0),
    Product(name="Vintage Watch", price=200.0)
    # Add more watches as needed
]

    db.session.add_all(watches)
    db.session.commit()

print("Watches added to the database.")
