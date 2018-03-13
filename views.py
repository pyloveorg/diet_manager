#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm
from models import Product

from flask import render_template, request, redirect


@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')


# jablko = Product(1, "jabłko", 46, 0, 0, 12)
# marchew = Product(2, "marchew", 27, 1, 0, 9)

# products_list = [jablko, marchew]


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

    products_list = Product.query.all()
    return render_template("products.html", products=products_list)


@app.route('/product/<ident>', methods=['GET', 'POST'])
def product_data(ident):
    product = Product.query.get(ident)
    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        return render_template("products.html", products=Product.query.all())

    return render_template("product.html", product=product, id=ident)
