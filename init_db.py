
from sqlalchemy import create_engine
from diet_manager import db
from diet_manager.models import User, Product


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

    product = Product()
    product.name = "jabłko"
    product.calories = 46
    product.protein = 0.4
    product.fat = 0.4
    product.carbohydrates = 12.1
    db.session.add(product)
    db.session.commit()

    product2 = Product()
    product2.name = "marchew"
    product2.calories = 27
    product2.protein = 1
    product2.fat = 0.2
    product2.carbohydrates = 8.7
    db.session.add(product2)
    db.session.commit()


if __name__ == '__main__':
    db_start()
