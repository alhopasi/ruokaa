from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.foods.models import Food, Ingredient, Like, Type
from application.foods.forms import NewFoodForm, MenuForm, FindField
from sqlalchemy import func
import random

@app.route("/foods/", methods=["GET"])
def foods_index():
    foods = Food.query.all()
    for f in foods:
        f.likes = f.countLikes()
        f.type = f.get_type_name()
    foods.sort(key = lambda f: f.likes, reverse = True)
    return render_template("foods/list.html", foods=foods, findField = FindField())

@app.route("/foods/", methods=["POST"])
def foods_index_filter():
    form = FindField(request.form)
    foods = Food.query.filter(func.lower(Food.name).like('%'+func.lower(form.name.data)+'%')).all()

    for f in foods:
        f.likes = f.countLikes()
        f.type = f.get_type_name()
    foods.sort(key = lambda f: f.likes, reverse = True)
    return render_template("foods/list.html", foods=foods, findField = form)

@app.route("/foods/<food_id>/", methods=["GET"])
def food_view(food_id):

    f = Food.query.get(food_id)
    if not f:
        return render_template("foods/food.html", food = None)

    i = f.findIngredients()
    u = f.getUser()
    r = 'none'
    t = Type.query.get(f.type_id).name
    if current_user.is_authenticated:
        r = current_user.get_role()
    return render_template("foods/food.html", food = f, ingredients = i, user = u, role = r, type = t)

@app.route("/foods/edit/<food_id>/", methods=["GET"])
@login_required
def food_edit(food_id):

    f = Food.query.get(food_id)
    if not f:
        return render_template("foods/update.html", food = None)

    form = NewFoodForm()
    form.duration.default = f.preparing_time
    food_type = Type.query.get(f.type_id)
    form.food_type.default = food_type.name
    form.process()
    
    u = f.getUser()

    r = 'none'
    if current_user.is_authenticated:
        r = current_user.get_role()

    form.name.data = f.name
    form.recipe.data = f.recipe

    form.ingredients.clear()
    for ingredient in f.findIngredients():
        form.ingredients.append(ingredient.get('name'))

    return render_template("foods/update.html", food = f, ingredients = form.ingredients, user = u, newFoodForm = form, role = r)

@app.route("/foods/menu/", methods=["GET"])
def foods_menu():
    return render_template("foods/menu.html", menuForm = MenuForm())

@app.route("/foods/menu/", methods=["POST"])
def foods_menu_create():
    form = MenuForm(request.form)
    foods = None
    if form.food_type.data == 'Kaikki':
        foods = Food.query.all()
    else:
        food_type = Type.query.filter_by(name=form.food_type.data).first()
        if food_type:
            foods = Food.query.filter_by(type_id=food_type.id).all()
            random.shuffle(foods)
            for f in foods:
                f.likes = f.countLikes()
                f.type = f.get_type_name()
                if f.likes < -4:
                    foods.remove(f)
    return render_template("foods/menu.html", menuForm = form, foods=foods)

@app.route("/foods/new/", methods=["GET"])
@login_required
def foods_form():
    newFoodForm = NewFoodForm()
    newFoodForm.ingredients.clear()
    return render_template("foods/new.html", newFoodForm = newFoodForm)

@app.route("/foods/new/", methods=["POST"])
@login_required
def foods_create():

    form = NewFoodForm(request.form)

    if request.form.get('remove_ingredient_button'):
        ingredient = request.form.get('remove_ingredient_button')
        form.ingredients.remove(ingredient)
        return render_template("foods/new.html", newFoodForm = form, ingredients=form.ingredients)

    form.ingredient.errors = []
    if request.form.get('add_ingredient_button') == '':
        if len(form.ingredient.data) < 3 or len(form.ingredient.data) > 20:
            form.ingredient.errors.append("Raaka-aineen tulee olla 3-20 kirjainta")
        elif form.ingredient.data in form.ingredients:
            form.ingredient.errors.append("Raaka-aine on jo lisätty")
        else:            
            form.ingredients.append(form.ingredient.data)
        form.ingredient.data = ''
        return render_template("foods/new.html", newFoodForm = form, ingredients=form.ingredients)

    if not form.validate() or not form.ingredients:
        if not form.ingredients:
            form.ingredient.errors.append("Ruoalla tulle olla vähintään yksi raaka-aine")
        return render_template("foods/new.html", newFoodForm = form, ingredients=form.ingredients)

    type_id = Type.find_type(form.food_type.data)

    f = Food(form.name.data, form.duration.data, form.recipe.data, current_user.id, type_id)

    for ingredient in form.ingredients:
        i = Ingredient.findIngredient(ingredient)
        f.ingredients.append(i)

    db.session().add(f)
    db.session().commit()

    return redirect(url_for("foods_index"))

@app.route("/foods/<food_id>/", methods=["POST"]) 
@login_required
def foods_update(food_id):
    f = Food.query.get(food_id)
    
    if not (f.account_id == current_user.id or current_user.get_role() == 'admin'):
        return redirect(url_for("food_edit", food_id=f.id))

    u = f.getUser()
    form = NewFoodForm(request.form)

    if request.form.get('remove_ingredient_button'):
        ingredient = request.form.get('remove_ingredient_button')
        form.ingredients.remove(ingredient)
        return render_template("foods/update.html", food=f, ingredients=form.ingredients, user=u, newFoodForm=form)

    form.ingredient.errors = []
    if request.form.get('add_ingredient_button') == '':
        if len(form.ingredient.data) < 3 or len(form.ingredient.data) > 20:
            form.ingredient.errors.append("Raaka-aineen tulee olla 3-20 kirjainta")
        elif form.ingredient.data in form.ingredients:
            form.ingredient.errors.append("Raaka-aine on jo lisätty")
        else:
            form.ingredients.append(form.ingredient.data)
        form.ingredient.data = ''
        return render_template("foods/update.html", food=f, ingredients=form.ingredients, user=u, newFoodForm=form)

    if not form.validate() or not form.ingredients:
        if not form.ingredients:
            form.ingredient.errors.append("Ruoalla tulle olla vähintään yksi raaka-aine")
        return render_template("foods/update.html", food=f, ingredients=form.ingredients, user=u, newFoodForm=form)


    f.name = form.name.data
    f.preparing_time = form.duration.data
    f.recipe = form.recipe.data

    f.type_id = Type.find_type(form.food_type.data)

    f.ingredients.clear()
    for ingredient in form.ingredients:
        i = Ingredient.findIngredient(ingredient)
        f.ingredients.append(i)

    db.session().commit()

    return redirect(url_for("food_view", food_id=f.id))

@app.route("/foods/<food_id>/<ingredient_id>")
@login_required
def foods_delete_ingredient(food_id, ingredient_id):
    f = Food.query.get(food_id)

    if not f.account_id == current_user.id:
        return redirect(url_for("food_edit", food_id=f.id))

    f.deleteIngredient(ingredient_id)
    return redirect(url_for("food_edit", food_id=food_id))


@app.route("/foods/delete/<food_id>")
@login_required
def foods_delete(food_id):

    f = Food.query.get(food_id)

    if not (f.account_id == current_user.id or current_user.get_role() == 'admin'):
        return redirect(url_for("foods_index"))

    Food.delete_food(food_id=food_id)

    return redirect(url_for("foods_index"))

@app.route("/foods/like/<food_id>?<value>")
@login_required
def foods_like(food_id, value):
    f = Food.query.get(food_id)
    u = current_user

    Like.query.filter_by(food_id=f.id, account_id=u.id).delete()
    l = Like(f.id, u.id, value)
    db.session().add(l)
    db.session().commit()

    return redirect(url_for("food_view", food_id=f.id))