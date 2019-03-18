from application import app, db
from flask import render_template, request, redirect, url_for
from application.foods.models import Food


@app.route("/foods/", methods=["GET"])
def foods_index():
    return render_template("foods/list.html", foods=Food.query.all())


@app.route("/foods/new/")
def foods_form():
    return render_template("foods/new.html")


@app.route("/foods/", methods=["POST"])
def foods_create():
    f = Food(request.form.get("name"), request.form.get("length"), request.form.get("recipe"))
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