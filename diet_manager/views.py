#!/usr/bin/env python
# encoding: utf-8
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from diet_manager import app
from diet_manager import db
from diet_manager import lm
from diet_manager.models import Product, Dish, Ingredient, DailyMeals, Portion, User

from flask import render_template, request, redirect, flash


@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    """
    if request.method is POST, new product is added to the database
    if request.method is GET, displays the list of products with the form to add new product
    """
    if request.method == "POST":
        name = request.form.get("nazwa")
        calories = request.form.get("kalorie")
        protein = request.form.get("bialko")
        fat = request.form.get("tluszcze")
        carbohydrates = request.form.get("weglowodany")
        if float(calories) < 0 or float(protein) < 0 or float(fat) < 0 or float(carbohydrates) < 0:
            flash("Musisz wpisać dodatnie wartości kalorii, białka, tłuszczy i węglowodanów")
            return redirect('/products')
        product = Product(name=name, calories=calories, protein=protein,
                          fat=fat, carbohydrates=carbohydrates)
        db.session.add(product)
        db.session.commit()

        return redirect("/products")

    products_list = Product.query.order_by(Product.name).all()
    return render_template("products.html", products=products_list)


@app.route('/product/<ident>', methods=['GET', 'POST'])
@login_required
def product_data(ident):
    """
    displays all the information about the product that has id equal to the parameter ident
    admin (and only admin) can delete product from the database
    :param ident: int
    """
    product = Product.query.get(ident)
    ingredient_list = Ingredient.query.filter(Ingredient.product_id == product.id).all()
    dish_id_list = []
    for ingredient in ingredient_list:
        dish_id_list.append(ingredient.dish_id)
    dish_list = Dish.query.filter(Dish.id.in_(dish_id_list)).all()

    # sq = db.session.query(Ingredient.query.with_entities(Ingredient.dish_id)
    #                       .filter(Ingredient.product_id == product.id)).subquery()
    # q = db.session.query(Dish).filter(Dish.id.in_(sq))

    # dish_list = []
    # for ingredient in ingredient_list:
    #     dish = Dish.query.filter(ingredient.dish_id == Dish.id).first()
    #     dish_list.append(dish)
    if request.method == "POST":
        if current_user.admin:
            db.session.delete(product)
            db.session.commit()
        else:
            flash('Nie masz uprawnień do usuwania produktów')
        return redirect("/products")

    return render_template("product.html", product=product, id=ident, dish_list=dish_list)


@app.route('/product/<ident>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(ident):
    """
    user can edit parameters of the product that has id equal to the parameter ident
    :param ident: int
    """
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
@login_required
def new_dish():
    """
    user can add new dish (only name)
    than is redirected to the page where can add ingredients to that dish
    """
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
@login_required
def new_ingredient(d_id):
    """
    user adds new ingredients to the dish that has id equal to the parameter d_id
    there are also displayed already added ingredients
    :param d_id: int
    """
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
    return render_template("add_ingredient.html", dish_id=d_id, products_list=products_list,
                           to_print=to_print, dish=dish)


@app.route('/dish/<d_id>', methods=['GET', 'POST'])
@login_required
def dish_data(d_id):
    """
    user can display all the information about the dish that has id equal to d_id
    if the dish has no ingredients - user is redirected to the page where he can add ingredients
    :param d_id: int
    """
    dish = Dish.query.get(d_id)
    to_print = []
    amount = 0
    for ingr in dish.ingredients:
        p_id = ingr.product_id
        p = Product.query.get(p_id)
        string_to_print = '{} - {} gramów'.format(p.name, ingr.amount)
        to_print.append(string_to_print)
        amount = dish.count_weight()
        parameters = dish.count_parameters()
    if amount == 0:
        flash('Ta potrawa nie ma żadnych składników. Proszę dodaj składniki.')
        return redirect('/dish/' + str(d_id) + '/add/ingredient')

    return render_template("dish.html", dish=dish, id=d_id, to_print=to_print, amount=amount, parameters=parameters)


@app.route('/list_of_dishes', methods=['GET'])
@login_required
def dishes():
    """
    user can display the list of all the dishes in the database
    """
    dishes_list = Dish.query.order_by(Dish.name).all()
    return render_template("list_of_dishes.html", list=dishes_list)


# @app.route('/dish/find/calories', methods=['GET', 'POST'])
# @login_required
# def find_calories():
#     if request.method == "POST":
#         min_calories = request.form.get("min_cal")
#         max_calories = request.form.get("max_cal")
#         dishes = Dish.query.filter(min_calories <= Dish.count_parameters() <= max_calories)
#
#         return redirect("/dish/find/calories")
#
#     return render_template("dish_calories")


@app.route('/dish/find/name', methods=['GET', 'POST'])
@login_required
def find_name():
    if request.method == "POST":
        name_to_find = request.form.get("name")
        found_dish = Dish.query.filter(Dish.name == name_to_find).first()
        if found_dish is None:
            flash('Nie ma takiej potrawy w naszej bazie.')
            flash('Możesz dodać nową potrawę albo poszukać innej potrawy')
            return redirect('/list_of_dishes')
        found_dish_id = found_dish.id
        return redirect('/dish/' + str(found_dish_id))
    return render_template("dish_find_name.html")


@app.route('/dish/find/product', methods=['GET', 'POST'])
@login_required
def find_by_product():
    if request.method == "POST":
        product_to_find = request.form.get("name")
        found_product = Product.query.filter(Product.name == product_to_find).first()
        if found_product is None:
            flash('Nie ma takiego produktu w naszej bazie.')
            flash('Możesz dodać nowy produkt albo poszukać innej potrawy')
            return redirect('/list_of_dishes')
        found_product_id = found_product.id
        return redirect('/product/' + str(found_product_id))
    return render_template("dish_find_product.html")


@app.route('/meal/add', methods=['GET', 'POST'])
@login_required
def new_meal():
    """
    user creates new day of meals by choosing a date
    user is redirected to the page where he can add portions of the dish that have been eaten on that day
    """
    if request.method == "POST":
        date = request.form.get("data")
        u_id = current_user.id
        meal_new = DailyMeals(date=date, user_id=u_id)
        try:
            db.session.add(meal_new)
            db.session.commit()
            m_id = meal_new.id
            link_name = '/meal/' + str(m_id) + '/add/portion'
            return redirect(link_name)
        except IntegrityError:
            flash('Już wpisywałeś posiłki w tym dniu. Jesli chcesz dodać coś nowego, to wybierz datę z listy')
            return redirect('/daily_meals')
    return render_template("add_meal.html")


@app.route('/meal/<m_id>/add/portion', methods=['GET', 'POST'])
@login_required
def new_portion(m_id):
    """
    user adds new portions of dishes that he has eaten during the day (id = m_id)
    if there are already added portions - they are displayed on the top of the page
    :param m_id: int
    """
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
        if len(Dish.query.get(dish).ingredients) == 0:
            flash("Ta potrawa nie ma żadnego składnika. Dodaj składniki.")
            return redirect("/dish/" + dish + "/add/ingredient")
        meal_id = m_id
        portion_new = Portion(amount=amount, dish_id=dish, meal_id=meal_id)
        db.session.add(portion_new)
        db.session.commit()
        link_name_1 = '/meal/' + str(meal_id) + '/add/portion'
        return redirect(link_name_1)
    return render_template("add_portion.html", meal_id=m_id, dish_list=dish_list, to_print=to_print, meal=meal)


@app.route('/meal/<m_id>', methods=['GET', 'POST'])
@login_required
def meal_data(m_id):
    """
    user can get information about his daily meal portions (m_id = meal.id)
    :param m_id: int
    """
    meal = DailyMeals.query.get(m_id)
    to_print = []
    parameters = 0
    for portion in meal.portions:
        d_id = portion.dish_id
        d = Dish.query.get(d_id)
        string_to_print = '{} - {} gramów'.format(d.name, portion.amount)
        to_print.append(string_to_print)
        parameters = meal.count_daily_parameters()
    if parameters == 0:
        flash('Nie dodałeś żadnego posiłku w dniu {}. Proszę dodaj posiłki.'.format(meal.date))
        return redirect('/meal/' + str(m_id) + '/add/portion')
    return render_template("meal.html", meal=meal, id=m_id, to_print=to_print, parameters=parameters)


@app.route('/meal/<m_id>/edit', methods=['GET'])
@login_required
def meal_edit(m_id):
    """
    user can delete the portion that he did not eat that day (m_id = meal.id)
    he is redirected to the page portion/<p_id>/delete
    :param m_id: int
    """
    edited_meal = DailyMeals.query.get(m_id)
    to_print = []
    list_of_links = []
    for portion in edited_meal.portions:
        d_id = portion.dish_id
        d = Dish.query.get(d_id)
        string_to_print = "{} - {} gramów".format(d.name, portion.amount)
        link = '/portion/{}/delete'.format(portion.id)
        to_print.append(string_to_print)
        list_of_links.append(link)
    n = len(to_print)
    return render_template("meal_edit.html", n=n, to_print=to_print, links=list_of_links, meal=edited_meal, id=m_id)


@app.route('/portion/<p_id>/delete', methods=['GET', 'POST'])
@login_required
def portion_delete(p_id):
    """
    the portion is deleted by the click on the page meal/<m_id>/edit
    :param p_id: int
    """
    portion_to_delete = Portion.query.get(p_id)
    db.session.delete(portion_to_delete)
    db.session.commit()
    return redirect("/daily_meals")


@app.route('/daily_meals', methods=['GET'])
@login_required
def list_of_meals():
    """
    list of dates when user added his meals
    """
    meals_list = DailyMeals.query.filter(DailyMeals.user_id == current_user.id).order_by(DailyMeals.date).all()
    return render_template("list_of_meals.html", list=meals_list, current_user=current_user)


@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))


@app.route('/user/register', methods=['GET', 'POST'])
def register_user():
    """
    new user can be registered (and added to the database) by filling the form
    """
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
        return redirect('/daily_meals')
    return render_template('user_register.html')


@app.route('/user/login', methods=['GET', 'POST'])
def login_user_dm():
    """
    user can log in to the application
    if user is already logged in - he is redirected to the page with the list of his meals
    """
    if current_user.is_authenticated:
        return redirect('/daily_meals')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()
        if not user:
            flash('Nie ma takiego użytkownika w bazie')
            return redirect('/user/login')
        if user.check_password(password):
            login_user(user)
            flash('Użytkownik zalogowany')
            return redirect('/daily_meals')
        flash('Zły e-mail lub hasło')
        return redirect('/user/login')
    return render_template('user_login.html')


@app.route('/logout')
def logout():
    """
    user can log out from the application
    """
    logout_user()
    flash('Użytkownik wylogowany')
    return redirect('user/login')
