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

jablko = Product(1, "jabłko", 46, 0, 0, 12)
marchew = Product(2, "marchew", 27, 1, 0, 9)

products_list = [jablko, marchew]

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == "POST":
        product_id = request.form.get("id")
        name = request.form.get("nazwa")
        calories = request.form.get("kalorie")
        protein = request.form.get("bialko")
        fat = request.form.get("tluszcze")
        carbohydrates = request.form.get("weglowodany")
        products_list.append(Product(product_id, name, calories, protein, fat, carbohydrates))
        return redirect("/products")

    return render_template("products.html", products=products_list)

@app.route('/product/<ident>', methods=['GET', 'POST'])
def product_data(ident):
    for product in products_list:
        if int(product.product_id) == int(ident):
            if request.method == "POST":
                products_list.remove(product)
                return render_template("products.html", products=products_list)

            return render_template("product.html", product=product, id=ident)



