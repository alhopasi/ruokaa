from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from application import app, db
from application.foods.models import Food, Like
from application.auth.models import User
from application.auth.forms import LoginForm, NewAccountForm, UpdateAccountForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())
    
    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "Käyttäjätunnusta tai salasanaa ei löydy")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/new/", methods = ["GET"])
def account_new():
    if not current_user.is_authenticated:
        return render_template("auth/new.html", newAccountForm = NewAccountForm())
    else:
        return redirect(url_for("index"))


@app.route("/auth/", methods=["POST"])
def account_create():
    form = NewAccountForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", newAccountForm = form)

    u = User(form.name.data, form.username.data, form.password.data)

    oldUser = User.query.filter_by(username=form.username.data).first()
    if oldUser:
        form.username.errors.append("käyttäjätunnus on jo olemassa")
        return render_template("auth/new.html", newAccountForm = form)

    u.set_role("user")

    if u.username == "admin":
        u.set_role("admin")

    db.session().add(u)
    db.session().commit()

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    login_user(user)

    return redirect(url_for("index"))

@app.route("/profile/", methods=["GET"])
@login_required
def auth_view_user():
    u = current_user
    pwd = "*" * len(u.password)
    f = Food.query.filter(Food.account_id == current_user.id).all()
    for food in f:
        food.likes = food.countLikes()
        food.type = food.get_type_name()
    f.sort(key = lambda f: f.likes, reverse = True)
    return render_template("auth/profile.html", user = u, pwd = pwd, foods = f)

@app.route("/profile/edit/", methods=["GET"])
@login_required
def auth_edit_user():
    u = current_user
    form = UpdateAccountForm(request.form)

    form.name.data = u.name
    form.username.data = u.username

    return render_template("auth/update.html", accountForm = form)

@app.route("/profile/edit/", methods=["POST"])
@login_required
def account_update():
    u = User.query.get(current_user.id)

    f = UpdateAccountForm(request.form)

    if not f.validate():
        return render_template("auth/update.html", accountForm = f)

    u.name = f.name.data
    
    oldUser = User.query.filter_by(username=f.username.data).first()
    if oldUser and (not oldUser.username == u.username):
        f.username.errors.append("käyttäjätunnus on jo olemassa")
        return render_template("auth/update.html", accountForm = f)
    
    u.username = f.username.data
    
    if (f.password.data):
        u.password = f.password.data

    db.session().commit()

    return redirect(url_for("auth_view_user"))

@app.route("/profile/delete")
@login_required
def delete_user():
    foods = Food.getUsersFoods(account_id=current_user.id)
    for food in foods:
        Food.delete_food(food_id=food.get('food_id'))
    
    Like.query.filter_by(account_id = current_user.id).delete()

    User.query.filter(User.id == current_user.id).delete()

    db.session().commit()
    
    logout_user()

    return redirect(url_for("index"))

@app.route("/users/")
@login_required
def list_users():
    foodCount = Food.getFoodCount()
    users = User.query.all()
    for user in users:
        user.food_count = 0
        for foodC in foodCount:
            if foodC.get('id') == user.id:
                user.food_count = foodC.get('foods')
                continue
                
    users.sort(key = lambda u: u.food_count, reverse = True)
    return render_template("auth/list.html", users=users)