
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

    product3 = Product()
    product3.name = "banan"
    product3.calories = 97
    product3.protein = 1
    product3.fat = 0.3
    product3.carbohydrates = 23.5
    db.session.add(product3)
    db.session.commit()

    product4 = Product()
    product4.name = "jajko"
    product4.calories = 140
    product4.protein = 12.5
    product4.fat = 9.7
    product4.carbohydrates = 0.6
    db.session.add(product4)
    db.session.commit()

    product5 = Product()
    product5.name = "pomidor"
    product5.calories = 15
    product5.protein = 0.9
    product5.fat = 0.2
    product5.carbohydrates = 3.6
    db.session.add(product5)
    db.session.commit()


if __name__ == '__main__':
    db_start()
