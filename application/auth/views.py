from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from application import app, db
from application.foods.models import Food
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

    form = UpdateAccountForm(request.form)

    return render_template("auth/profile.html", user = u, accountForm = form, pwd = pwd)

@app.route("/profile/", methods=["POST"])
@login_required
def account_update():
    u = User.query.get(current_user.id)

    f = UpdateAccountForm(request.form)
    pwd = "*" * len(u.password)

    if not f.validate():
        return render_template("auth/profile.html", accountForm = f, user = u, pwd = pwd)


    if (f.name.data):
        u.name = f.name.data
    if (f.username.data):
        oldUser = User.query.filter_by(username=f.username.data).first()
        if oldUser:
            f.username.errors.append("käyttäjätunnus on jo olemassa")
            return render_template("auth/profile.html", accountForm = f, user = u, pwd = pwd)
        u.username = f.username.data
    if (f.password.data):
        u.password = f.password.data

    db.session().commit()

    return redirect(url_for("auth_view_user"))

@app.route("/profile/delete")
@login_required
def delete_user():
    User.query.filter(User.id == current_user.id).delete()
    db.session().commit()
    
    logout_user()

    return redirect(url_for("index"))

@app.route("/users/")
@login_required
def list_users():
    foodCount = Food.getFoodCount()
    return render_template("auth/list.html", users=User.query.all(), foodCount = foodCount)