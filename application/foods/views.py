from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.foods.models import Food, Ingredient
from application.foods.forms import NewFoodForm, UpdateFoodForm


@app.route("/foods/", methods=["GET"])
def foods_index():
    return render_template("foods/list.html", foods=Food.query.all())


@app.route("/foods/<food_id>/", methods=["GET"])
def food_view(food_id):

    f = Food.query.get(food_id)
    if not f:
        return render_template("foods/food.html", food = None)

    i = f.findIngredients()
    u = f.getUser()
    return render_template("foods/food.html", food = f, ingredients = i, user = u, updateFoodForm = UpdateFoodForm())

@app.route("/foods/new/")
@login_required
def foods_form():
    return render_template("foods/new.html", newFoodForm = NewFoodForm())


@app.route("/foods/", methods=["POST"])
@login_required
def foods_create():

    form = NewFoodForm(request.form)

    if not form.validate():
        return render_template("foods/new.html", newFoodForm = form)

    f = Food(form.name.data, form.duration.data, form.recipe.data, current_user.id)

    # tarkista, että löytyykö jo ruoka-aineet, jos ei, luo uudet. tee monesta-moneen suhteet.
    i1 = Ingredient.findIngredient(form.ingredient1.data)
    i2 = Ingredient.findIngredient(form.ingredient2.data)
    i3 = Ingredient.findIngredient(form.ingredient3.data)
    i4 = Ingredient.findIngredient(form.ingredient4.data)

    f.ingredients.append(i1)
    if i2:
        f.ingredients.append(i2)
    if i3:
        f.ingredients.append(i3)
    if i4:
        f.ingredients.append(i4)

    db.session().add(f)
    db.session().commit()

    return redirect(url_for("foods_index"))


@app.route("/foods/<food_id>/", methods=["POST"])
@login_required
def foods_set_name(food_id):
    f = Food.query.get(food_id)
    f.name = request.form.get("name")
    db.session().commit()

    return redirect(url_for("foods_index"))

@app.route("/foods/food/", methods=["POST"])
@login_required
def foods_update(food, ingredients, user):
    return render_template("foods/food.html", food = f, ingredients = i, user = u)
def food_delete_ingredient(food_id, ingredient_id):
    return redirect(url_for("food_view", food_id=food.id))


@app.route("/foods/delete/<food_id>")
@login_required
def food_delete():
    # User.query.filter(User.id == current_user.id).delete()
    # db.session().commit()
    
    # logout_user()

    return redirect(url_for("foods_index"))