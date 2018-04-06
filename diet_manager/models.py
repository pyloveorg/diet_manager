from sqlalchemy.orm import relationship

__author__ = ''

from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import Date
from sqlalchemy.types import Float

from werkzeug.security import generate_password_hash, check_password_hash

from diet_manager import db


class User(db.Model, UserMixin):
    """
    User model for reviewers.
    :type id: int, autoincrement
    :type email: email, unique
    :type name: str
    :type password_hash: str
    :type weight: int
    :type height: int
    :type active: bool
    :type admin: bool
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(200), unique=True)
    name = Column(String(20))
    password_hash = db.Column(db.String(128), default="")
    weight = Column(Integer, default=0)
    height = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    patron = Column(Boolean, default=False)

    def is_active(self):
        """
        Returns if user is active.
        """
        return self.active

    def is_admin(self):
        """
        Returns if user is admin.
        """
        return self.admin

    def set_password(self, password):
        """
        Generates new password hash for new user
        :param password:
        :return: hashed password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the password is correct by comparing hashed password from the database
        with the password written by the user
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    """
    class Product says about energetic values for all the products that
    our User can use to prepare his dishes
    :type id : int autoincrement
    :type name : string
    :type calories : int
    :type protein : int
    :type fat : int
    :type carbohydrates : int
    """
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)

    def __repr__(self):
        return "{}: {} kalorii, {} białka, {} tłuszczy, {} węglowodanów". \
            format(self.name, self.calories, self.protein, self.fat, self.carbohydrates)


class Ingredient(db.Model):
    """
       class Ingredient says how much of product do we have to use to prepare our dish
       :type product_id : Product
       :type amount : float
       """

    __tablename__ = 'ingredients'
    id = Column(Integer, autoincrement=True, primary_key=True)
    amount = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    dish_id = Column(Integer, ForeignKey('dish.id'))

    # def __repr__(self):
    #     return "{} - {} g".format(self.product_id.name, self.amount)


class Dish(db.Model):
    """
    class Dish is a list of products used to prepare that dish
    :type id : int autoincrement
    :type name : str
    """

    __tablename__ = 'dish'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    ingredients = relationship("Ingredient")

    def count_weight(self):
        """
        method count_weight is used to count the total weight of the Dish
        by adding the amounts of all the ingredients
        :return: float
        """
        amount = 0
        for ingredient in self.ingredients:
            amount += ingredient.amount
        return amount

    def count_parameters(self):
        """
        method count_parameters is used to count how much calories, protein, fat and carbohydrates
        contains 100 g of the Dish
        :return: tuple (calories, protein, fat, carbohydrates)
        """
        calories = 0
        protein = 0
        fat = 0
        carbohydrates = 0
        for ingredient in self.ingredients:
            p = Product.query.get(ingredient.product_id)
            calories += p.calories * ingredient.amount / 100
            protein += p.protein * ingredient.amount / 100
            fat += p.fat * ingredient.amount / 100
            carbohydrates += p.carbohydrates * ingredient.amount / 100
        calories = round(calories * 100 / self.count_weight(), 2)
        protein = round(protein * 100 / self.count_weight(), 2)
        fat = round(fat * 100 / self.count_weight(), 2)
        carbohydrates = round(carbohydrates * 100 / self.count_weight(), 2)
        return calories, protein, fat, carbohydrates


class Portion(db.Model):
    """
    class Portion says about the amount of the dish that has been eaten by the User during one Meal
   :type dish_id : Dish
   :type amount : float
   """

    __tablename__ = 'portion'
    id = Column(Integer, autoincrement=True, primary_key=True)
    amount = Column(Float, nullable=False)
    dish_id = Column(Integer, ForeignKey('dish.id'))
    meal_id = Column(Integer, ForeignKey('meal.id'))


class DailyMeals(db.Model):
    """
    class DailyMeals is used to present the list of all the Portions of the Dish that had been
    eaten by the User during one day
    :type date : datetime
    :type user_id : User
    """

    __tablename__ = 'meal'
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    portions = relationship("Portion")
    __table_args__ = (UniqueConstraint('user_id', 'date', name='date'),)

    def count_daily_parameters(self):
        """
        method count_daily_parameters is used to count: amount, calories, protein, fat and carbohydrates
        for all the Portions eaten by the User during one day

        :return: tuple (amount, calories, protein, fat, carbohydrates)
        """
        amount = 0
        calories = 0
        protein = 0
        fat = 0
        carbohydrates = 0
        for portion in self.portions:
            d = Dish.query.get(portion.dish_id)
            amount += portion.amount
            calories += d.count_parameters()[0] * portion.amount / 100
            protein += d.count_parameters()[1] * portion.amount / 100
            fat += d.count_parameters()[2] * portion.amount / 100
            carbohydrates += d.count_parameters()[3] * portion.amount / 100
        return amount, round(calories, 2), round(protein, 2), round(fat, 2), round(carbohydrates, 2)
