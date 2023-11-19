from database.models import db, Watch

watches = [
    Watch(name="Classic Watch", price=250.0),
    Watch(name="Modern Watch", price=300.0),
    Watch(name="Vintage Watch", price=200.0)
    # Add more watches as needed
]

db.session.add_all(watches)
db.session.commit()

print("Watches added to the database.")
