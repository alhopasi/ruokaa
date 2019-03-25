from application import app, db
from flask import render_template, request, redirect, url_for
from application.foods.models import Food
from application.foods.forms import NewFoodForm


@app.route("/foods/", methods=["GET"])
def foods_index():
    return render_template("foods/list.html", foods=Food.query.all())


@app.route("/foods/new/")
def foods_form():
    return render_template("foods/new.html", newFoodForm = NewFoodForm())


@app.route("/foods/", methods=["POST"])
def foods_create():
    form = NewFoodForm(request.form)

    if not form.validate():
        return render_template("foods/new.html", newFoodForm = form)

    f = Food(form.name.data, form.duration.data, form.recipe.data)
    db.session().add(f)
    db.session().commit()

    return redirect(url_for("foods_index"))


@app.route("/foods/<food_id>/", methods=["POST"])
def foods_set_name(food_id):
    print("Changing name!")
    f = Food.query.get(food_id)
    f.name = request.form.get("name")
    db.session().commit()

    return redirect(url_for("foods_index"))