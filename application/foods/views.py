from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.foods.models import Food, Ingredient, Like
from application.foods.forms import NewFoodForm


@app.route("/foods/", methods=["GET"])
def foods_index():
    foods = Food.query.all()
    return render_template("foods/list.html", foods=Food.query.all())


@app.route("/foods/<food_id>/", methods=["GET"])
def food_view(food_id):

    f = Food.query.get(food_id)
    if not f:
        return render_template("foods/food.html", food = None)

    i = f.findIngredients()
    u = f.getUser()
    return render_template("foods/food.html", food = f, ingredients = i, user = u)

@app.route("/foods/edit/<food_id>/", methods=["GET"])
def food_edit(food_id):

    f = Food.query.get(food_id)
    if not f:
        return render_template("foods/update.html", food = None)

    form = NewFoodForm()
    form.duration.default = f.preparing_time
    form.process()
    
    i = f.findIngredients()
    u = f.getUser()

    form.name.data = f.name
    form.recipe.data = f.recipe
    ingredients_size = len(i)
    form.ingredient1.data = i[0].get("name")
    if ingredients_size >= 2:
        form.ingredient2.data = i[1].get("name")
    if ingredients_size >= 3:
        form.ingredient3.data = i[2].get("name")
    if ingredients_size >= 4:
        form.ingredient4.data = i[3].get("name")
    

    return render_template("foods/update.html", food = f, ingredients = i, user = u, newFoodForm = form)

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
    if i2 and not (i2 == i1):
        f.ingredients.append(i2)
    if i3 and not (i3 == (i2 or i1)):
        f.ingredients.append(i3)
    if i4 and not (i4 == (i3 or i2 or i1)):
        f.ingredients.append(i4)

    db.session().add(f)
    db.session().commit()

    return redirect(url_for("foods_index"))

@app.route("/foods/<food_id>/", methods=["POST"]) 
@login_required
def foods_update(food_id):
    f = Food.query.get(food_id)
    
    if not f.account_id == current_user.id:
        return redirect(url_for("food_edit", food_id=f.id))

    i = f.findIngredients()
    u = f.getUser()
    form = NewFoodForm(request.form)
    
    if not form.validate():
        return render_template("foods/update.html", food=f, ingredients=i, user=u, newFoodForm=form)

    f.name = form.name.data
    f.preparing_time = form.duration.data
    f.recipe = form.recipe.data
    
    i1 = Ingredient.findIngredient(form.ingredient1.data)
    i2 = Ingredient.findIngredient(form.ingredient2.data)
    i3 = Ingredient.findIngredient(form.ingredient3.data)
    i4 = Ingredient.findIngredient(form.ingredient4.data)
    
    f.ingredients = []
    f.ingredients.append(i1)
    if i2 and not (i2 == i1):
        f.ingredients.append(i2)
    if i3 and not (i3 == (i2 or i1)):
        f.ingredients.append(i3)
    if i4 and not (i4 == (i3 or i2 or i1)):
        f.ingredients.append(i4)

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

    if not f.account_id == current_user.id:
        return redirect(url_for("foods_index"))

    i = f.findIngredients()
    for ingredient in i:
        f.deleteIngredient(ingredient['id'])
    Food.query.filter(Food.id == food_id).delete()
    db.session().commit()

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