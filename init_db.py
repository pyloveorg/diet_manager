
from sqlalchemy import create_engine
from diet_manager import db
from diet_manager.models import User


def db_start():
    create_engine('sqlite:///diet_manager.db', convert_unicode=True)

    user = User()
    user.name = "krystyna"
    user.email = 'mariquita1@wp.pl'
    user.set_password('superhaslo')
    user.weight = 50
    user.height = 150
    user.admin = True
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    db_start()
