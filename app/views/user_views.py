import json

from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import current_user, logout_user

from app.forms import SignupForm, LoginForm
from app.controllers.menu_controllers import get_menu_items
from app.controllers.payment_controllers import get_checkout_url, resolve_payment
from app.controllers.auth_controllers import (
    login_response,
    signup_response,
    login_required,
)

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/")
@users_blueprint.route("/home")
def home():
    return render_template("index.html")


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and current_user.get_role() == "customer":
        return redirect(url_for("users.menu"))

    form = LoginForm()
    return login_response(form)


@users_blueprint.route("/logout")
@login_required("customer")
def logout():
    logout_user()
    return redirect(url_for("users.home"))


@users_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated and current_user.get_role() == "customer":
        return redirect(url_for("users.menu"))
    form = SignupForm()
    return signup_response(form)


@users_blueprint.route("/menu")
@login_required("customer")
def menu():
    tx_ref = request.args.get("tx_ref")
    if tx_ref:
        try:
            result = resolve_payment(tx_ref)
            if result is True:
                # payment was successful
                flash(
                    "Your payment was processed successfully. your order has been queued.",
                    "success",
                )
            elif result is False:
                # payment has failed
                flash("There was an issue processing your payment.", "error")
            elif result is None:
                flash("Payment is pending, refresh this page to see updates.")
        except Exception as e:
            pass

    menu_items = get_menu_items()
    return render_template("menu/menu.html", menu_items=menu_items)


@users_blueprint.route("/order", methods=["POST"])
@login_required("customer")
def order():
    order_items = json.loads(request.form.get("order"))
    checkout_url = get_checkout_url(order_items)
    return redirect(checkout_url)


@users_blueprint.route("/order_history")
@login_required("customer")
def order_history():
    return render_template("placeholder.html")
