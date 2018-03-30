#!/usr/bin/env python
# encoding: utf-8
from flask_login import current_user, login_user, logout_user

from diet_manager import app
from diet_manager import db
from diet_manager import lm
from diet_manager.models import Product, Dish, Ingredient, DailyMeals, Portion, User

from flask import render_template, request, redirect, flash


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
    dish = Dish.query.get(d_id)
    to_print = []
    for ingr in dish.ingredients:
        p_id = ingr.product_id
        p = Product.query.get(p_id)
        string_to_print = '{} - {} gramów'.format(p.name, ingr.amount)
        to_print.append(string_to_print)
    if request.method == "POST":
        amount = request.form.get("ilosc")
        product = request.form.get("product")
        dish_id = d_id
        ingredient_new = Ingredient(amount=amount, dish_id=dish_id, product_id=product)
        db.session.add(ingredient_new)
        db.session.commit()
        link_name_1 = '/dish/' + str(dish_id) + '/add/ingredient'
        return redirect(link_name_1)
    return render_template("add_ingredient.html", dish_id=d_id, products_list=products_list, to_print=to_print)


@app.route('/dish/<d_id>', methods=['GET', 'POST'])
def dish_data(d_id):
    dish = Dish.query.get(d_id)
    to_print = []
    for ingr in dish.ingredients:
        p_id = ingr.product_id
        p = Product.query.get(p_id)
        string_to_print = '{} - {} gramów'.format(p.name, ingr.amount)
        to_print.append(string_to_print)
        amount = dish.count_weight()
        parameters = dish.count_parameters()
    return render_template("dish.html", dish=dish, id=d_id, to_print=to_print, amount=amount, parameters=parameters)


@app.route('/list_of_dishes', methods=['GET'])
def dishes():
    dishes_list = Dish.query.order_by(Dish.name).all()
    return render_template("list_of_dishes.html", list=dishes_list)


@app.route('/meal/add', methods=['GET', 'POST'])
def new_meal():
    if request.method == "POST":
        date = request.form.get("data")
        # db_date =
        meal_new = DailyMeals(date=date)
        db.session.add(meal_new)
        db.session.commit()
        m_id = meal_new.id
        link_name = '/meal/' + str(m_id) + '/add/portion'
        return redirect(link_name)
    return render_template("add_meal.html")


@app.route('/meal/<m_id>/add/portion', methods=['GET', 'POST'])
def new_portion(m_id):
    dish_list = Dish.query.order_by(Dish.name).all()
    meal = DailyMeals.query.get(m_id)
    to_print = []
    for portion in meal.portions:
        d_id = portion.dish_id
        d = Dish.query.get(d_id)
        string_to_print = '{} - {} gramów'.format(d.name, portion.amount)
        to_print.append(string_to_print)
    if request.method == "POST":
        amount = request.form.get("ilosc")
        dish = request.form.get("dish")
        meal_id = m_id
        portion_new = Portion(amount=amount, dish_id=dish, meal_id=meal_id)
        db.session.add(portion_new)
        db.session.commit()
        link_name_1 = '/meal/' + str(meal_id) + '/add/portion'
        return redirect(link_name_1)
    return render_template("add_portion.html", meal_id=m_id, dish_list=dish_list, to_print=to_print, meal=meal)


@app.route('/meal/<m_id>', methods=['GET', 'POST'])
def meal_data(m_id):
    meal = DailyMeals.query.get(m_id)
    to_print = []
    for portion in meal.portions:
        d_id = portion.dish_id
        d = Dish.query.get(d_id)
        string_to_print = '{} - {} gramów'.format(d.name, portion.amount)
        to_print.append(string_to_print)
        parameters = meal.count_daily_parameters()

    return render_template("meal.html", meal=meal, id=m_id, to_print=to_print, parameters=parameters)


@app.route('/daily_meals', methods=['GET'])
def list_of_meals():
    meals_list = DailyMeals.query.order_by(DailyMeals.date).all()
    return render_template("list_of_meals.html", list=meals_list)


@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))


@app.route('/user/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        weight = request.form.get('weight')
        height = request.form.get('height')
        new_user = User(name=name, email=email, weight=weight, height=height)
        new_user.set_password(password)
        flash('New user registered')
        db.session.add(new_user)
        db.session.commit()
        return redirect('/list_of_dishes')
    return render_template('user_register.html')


@app.route('/user/login', methods = ['GET', 'POST'])
def login_user_dm():
    if current_user.is_authenticated:
        return redirect('/daily_meals')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()
        if user.check_password(password):
            login_user(user)
            flash('Użytkownik zalogowany')
            return redirect('/daily_meals')
        flash('Zły e-mail lub hasło')
        return redirect('/user/login')
    return render_template('user_login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Użytkownik wylogowany')
    return redirect('user/login')


