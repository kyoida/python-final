from flaskapp import app
from database.models import db, Product

try:
    with app.app_context():
        with app.app_context():
            watches = [
                Product(name="Classic Watch", description="hello", price=250.0),
                Product(name="Modern Watch", price=300.0),
                Product(name="Vintage Watch", price=200.0)
                # Add more watches as needed
            ]
        db.session.add_all(watches)
        db.session.commit()
except Exception as e:
    print(f"Error adding watches to the database: {e}")


