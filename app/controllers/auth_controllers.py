from functools import wraps
from http import HTTPStatus
from urllib.parse import urlsplit

from flask import url_for, redirect, flash, render_template, request, current_app
from flask_login import current_user
import sqlalchemy as sa

from app import db
from app.models import User
from flask_login import login_user


def login_response(form):
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        if (
            user
            and user.get_role() == "customer"
            and user.check_password(form.password.data)
        ):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("users.menu")
            return redirect(next_page)

        flash("Login unsuccessful. Please check username and password", "danger")
        return (
            render_template("auth/login.html", title="Login", form=form),
            HTTPStatus.BAD_REQUEST,
        )

    return render_template("auth/login.html", title="Login", form=form)


def signup_response(form):
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Congratulations, you are now a registered user!", "success")
        return redirect(url_for("users.login"))

    return render_template("auth/signup.html", title="Signup", form=form)


def admin_login_response(form):
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        if (
            user
            and user.get_role() == "admin"
            and user.check_password(form.password.data)
        ):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("admin.admin_panel")
            return redirect(next_page)

        flash("Login unsuccessful. Please check username and password", "danger")
        return (
            render_template("auth/login.html", title="Login", form=form, admin=True),
            HTTPStatus.BAD_REQUEST,
        )

    return render_template("auth/login.html", title="Login", form=form, admin=True)


# https://stackoverflow.com/a/15884811
def login_required(role="any"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            urole = current_user.get_role()
            if (urole != role) and (role != "any"):
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
