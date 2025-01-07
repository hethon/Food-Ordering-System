from http import HTTPStatus

from flask import render_template, redirect, url_for, Blueprint, request
from flask_login import current_user, logout_user

from app.forms import LoginForm
from app.controllers.auth_controllers import admin_login_response, login_required
from app.controllers.menu_controllers import (
    get_menu_items,
    get_active_orders,
    set_menu_item_availability,
)


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.route("/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and current_user.get_role() == "admin":
        return redirect(url_for("admin.admin_panel"))

    form = LoginForm()
    return admin_login_response(form)


@admin_blueprint.route("/logout")
@login_required("admin")
def admin_logout():
    logout_user()
    return redirect(url_for("users.home"))


@admin_blueprint.route("/")
@admin_blueprint.route("/panel")
@login_required("admin")
def admin_panel():
    menu_items = get_menu_items()
    orders = get_active_orders()
    return render_template("admin/panel.html", menu_items=menu_items, orders=orders)


@admin_blueprint.route("/changeMenuItemAvailability", methods=["POST"])
@login_required("admin")
def change_menu_item_availability():
    menu_item = request.json
    try:
        set_menu_item_availability(
            menu_item_id=menu_item["menuItemId"], new_state=menu_item["newState"]
        )
    except Exception as e:
        return {"ok": False, "message": str(e)}, HTTPStatus.BAD_REQUEST
    else:
        return {"ok": True, "message": "success"}
