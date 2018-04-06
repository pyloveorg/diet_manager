
from sqlalchemy import create_engine
from diet_manager import db
from diet_manager.models import User


def db_start():
    create_engine('sqlite:///diet_manager.db', convert_unicode=True)
    db.create_all()
    db.session.commit()

    user = User()
    user.name = "krystyna"
    user.email = 'mariquita1@wp.pl'
    user.set_password('superhaslo')
    user.weight = 50
    user.height = 150
    user.admin = True
    user.patron = True
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    db_start()
