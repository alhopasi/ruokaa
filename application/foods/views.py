from application import app, db
from flask import render_template, request
from application.foods.models import Food

@app.route("/foods/new/")
def foods_form():
    return render_template("foods/new.html")

@app.route("/foods/", methods=["POST"])
def foods_create():
    f = Food(request.form.get("name"), request.form.get("length"), request.form.get("recipe"))
    db.session().add(f)
    db.session().commit()

    return "lisätty onnistuneesti!"

@app.route("/foods/", methods=["GET"])
def foods_index():
  return render_template("foods/list.html", foods = Food.query.all())