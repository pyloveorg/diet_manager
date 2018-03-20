from sqlalchemy.orm import relationship

__author__ = 'Piotr Dyba'

from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import Date
from sqlalchemy.types import Float


from main import db


class User(db.Model, UserMixin):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    email = Column(String(200), unique=True)
    password = Column(String(200), default='')
    admin = Column(Boolean, default=False)

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
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbohydrates = Column(Float)

    def __repr__(self):
        return "{}: {} kalorii, {} białka, {} tłuszczy, {} węglowodanów".\
            format(self.name, self.calories, self.protein, self.fat, self.carbohydrates)


class Ingredient(db.Model):
    """
       class Ingredient says how much of product do we have to use to prepare our dish
       :type product_id : Product
       :type amount : float
       """

    __tablename__ = 'ingredients'
    id = Column(Integer, autoincrement=True, primary_key=True)
    amount = Column(Float)
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
    name = Column(String(50), unique=True)
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
            calories += p.calories*ingredient.amount/100
            protein += p.protein*ingredient.amount/100
            fat += p.fat*ingredient.amount/100
            carbohydrates += p.carbohydrates*ingredient.amount/100
        calories = round(calories*100/self.count_weight(), 2)
        protein = round(protein*100/self.count_weight(), 2)
        fat = round(fat*100/self.count_weight(), 2)
        carbohydrates = round(carbohydrates*100/self.count_weight(), 2)
        return calories, protein, fat, carbohydrates

#
# class Portion(db.Model):
#     """
#     class Portion says about the amount of the dish that has been eaten by the User during one Meal
#    :type dish_id : Dish
#    :type amount : float
#    """
#
#     __tablename__ = 'portion'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     amount = Column(Float)
#     dish_id = Column(Integer, ForeignKey('dish.id'))
#     meal_id = Column(Integer, ForeignKey('meal.id'))
#
#
# class DailyMeals(db.Model):
#     """
#     class DailyMeals is used to present the list of all the Portions of the Dish that had been
#     eaten by the User during one day
#     :type date : datetime
#     :type user : User
#     """
#
#     __tablename__ = 'meal'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     date = Column(Date)
#     portions = relationship("Portion")
#