#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm
from models import Product, Dish, Ingredient

from flask import render_template, request, redirect


@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == "POST":
        name = request.form.get("nazwa")
        calories = request.form.get("kalorie")
        protein = request.form.get("bialko")
        fat = request.form.get("tluszcze")
        carbohydrates = request.form.get("weglowodany")
        product = Product(name=name, calories=calories, protein=protein,
                          fat=fat, carbohydrates=carbohydrates)
        db.session.add(product)
        db.session.commit()

        return redirect("/products")

    products_list = Product.query.order_by(Product.name).all()
    return render_template("products.html", products=products_list)


@app.route('/product/<ident>', methods=['GET', 'POST'])
def product_data(ident):
    product = Product.query.get(ident)
    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        return redirect("/products")

    return render_template("product.html", product=product, id=ident)


@app.route('/product/<ident>/edit', methods=['GET', 'POST'])
def product_edit(ident):
    edited_product = Product.query.get(ident)
    if request.method == "POST":
        edited_product.name = request.form.get("nazwa")
        edited_product.calories = request.form.get("kalorie")
        edited_product.protein = request.form.get("bialko")
        edited_product.fat = request.form.get("tluszcze")
        edited_product.carbohydrates = request.form.get("weglowodany")
        db.session.commit()
        return redirect("/products")

    return render_template("product_edit.html", product=edited_product, id=ident)


@app.route('/dish/add', methods=['GET', 'POST'])
def new_dish():
    if request.method == "POST":
        name = request.form.get("nazwa")
        dish_new = Dish(name=name)
        db.session.add(dish_new)
        db.session.commit()
        d_id = dish_new.id
        link_name = '/dish/' + str(d_id) + '/add/ingredient'
        return redirect(link_name)
    return render_template("add_dish.html")


@app.route('/dish/<d_id>/add/ingredient', methods=['GET', 'POST'])
def new_ingredient(d_id):
    products_list = Product.query.order_by(Product.name).all()
    if request.method == "POST":
        amount = request.form.get("ilosc")
        product = request.form.get("product")
        dish_id = d_id
        ingredient_new = Ingredient(amount=amount, dish_id=dish_id, product_id=product)
        db.session.add(ingredient_new)
        db.session.commit()
        link_name_1 = '/dish/' + str(dish_id) + '/add/ingredient'
        return redirect(link_name_1)
    return render_template("add_ingredient.html", dish_id=d_id, products_list=products_list)


@app.route('/dish/<d_id>', methods=['GET', 'POST'])
def dish_data(d_id):
    dish = Dish.query.get(d_id)
    to_print = []
    for ingr in dish.ingredients:
        p_id = ingr.product_id
        p = Product.query.get(p_id)
        string_to_print = '{} - {} gramów'.format(p.name, ingr.amount)
        to_print.append(string_to_print)
    return render_template("dish.html", dish=dish, id=d_id, to_print=to_print)


@app.route('/list_of_dishes', methods=['GET'])
def dishes():
    dishes_list = Dish.query.order_by(Dish.name).all()
    return render_template("list_of_dishes.html", list=dishes_list)
