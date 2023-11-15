from .models import web, db


def add_user(user:web)->None:
    db.session.add(user)
    db.session.commit()

def delete_user(user:web)->None:
    db.session.delete(user)
    db.session.commit()

def get_all_users()->db.Query:
    return web.query.all()
