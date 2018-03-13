__author__ = 'Piotr Dyba'

from flask_login import UserMixin

from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean

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


class Product:
    """
    class Product says about energetic values for all the products that
    our User can use to prepare his dishes
    :type product_id : int autoincrement
    :type name : string
    :type calories : int
    :type protein : int
    :type fat : int
    :type carbohydrates : int
    :type list_of_dishes : list of Dish
    """

    def __init__(self, product_id, name, calories, protein, fat, carbohydrates):
        self.list_of_dishes = []
        self.carbohydrates = carbohydrates
        self.fat = fat
        self.protein = protein
        self.calories = calories
        self.name = name
        self.product_id = product_id

    def __str__(self):
        return "{}: {} kalorii, {} białka, {} tłuszczy, {} węglowodanów".\
            format(self.name, self.calories, self.protein, self.fat, self.carbohydrates)