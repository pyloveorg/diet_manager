from sqlalchemy.orm import relationship

__author__ = 'Piotr Dyba'

from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
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

    def __repr__(self):
        return "{} g produktu {}".format(self.amount, self.product_id.name)


class Dish(db.Model):
    """
    class Dish is a list of products used to prepare that dish
    :type dish_id : int autoincrement
    :type name : str
    """

    __tablename__ = 'dish'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    ingredient = relationship("Ingredient")
