import os
from uuid import uuid4
import requests

from flask_login import current_user
import sqlalchemy as sa

from app import db
from app.models import MenuItem, Order, OrderItem, Payment
from .menu_controllers import all_menu_items_available


CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")


def _get_menu_items(order_items):
    """return a list of MenuItem from the given order_items"""

    menu_items = [db.session.get(MenuItem, item["id"]) for item in order_items]

    if not all(menu_items):
        # some order items doesn't exist
        raise Exception("Order contains items that doesn't exist.")
    return menu_items


def _calculate_total_price(order_items, menu_items):
    """calculate the total price of an order"""

    total_price = 0
    for order_item, menu_item in zip(order_items, menu_items):
        order_quantity = order_item["quantity"]
        unit_price = menu_item.price
        order_price = order_quantity * unit_price
        total_price += order_price

    return total_price


def _add_order(total_price, owner):
    """Add order to database session and return it"""

    order = Order(total_price=total_price, status="pending", owner=owner)
    db.session.add(order)

    return order


def _add_order_items(order_items, menu_items, order):
    """Add order_items to database session"""

    for order_item, menu_item in zip(order_items, menu_items):
        order_quantity = order_item["quantity"]
        unit_price = menu_item.price
        order_price = order_quantity * unit_price
        db.session.add(
            OrderItem(
                quantity=order_quantity,
                price=order_price,
                menu_item=menu_item,
                order=order,
            )
        )


def _register_order(order_items, owner):
    """takes care of adding order into database"""

    menu_items = _get_menu_items(order_items)

    if not all_menu_items_available(menu_items):
        raise Exception("One of the ordered items is not available at the moment.")

    total_price = _calculate_total_price(order_items, menu_items)
    order = _add_order(total_price, owner=owner)
    _add_order_items(order_items, menu_items, order=order)

    return order


def _initialize_payment(order, tx_ref, owner):
    payment = Payment(
        amount=order.total_price,
        status="pending",
        tx_ref=tx_ref,
        owner=owner,
        order=order,
    )
    db.session.add(payment)


def get_checkout_url(order_items):
    tx_ref = f"FOS{uuid4().hex}"

    order = _register_order(order_items, current_user)
    _initialize_payment(order, tx_ref, current_user)

    db.session.commit()

    payload = {
        "amount": str(order.total_price),
        "currency": "ETB",
        "email": current_user.email,
        "tx_ref": tx_ref,
        "return_url": f"{os.getenv("ROOT_URL")}/menu?tx_ref={tx_ref}",
        "customization": {
            "title": "FOS",
            "description": "Food Ordering System",
        },
    }
    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.chapa.co/v1/transaction/initialize",
        json=payload,
        headers=headers,
    )
    checkout_url = response.json()["data"]["checkout_url"]

    return checkout_url


def resolve_payment(tx_ref):
    """return True if payment was successful, False if it failed, None if neither has happened"""

    url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    payload = ""
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    response = requests.get(url, headers=headers, data=payload)
    status = response.json().get("status")

    query = sa.select(Payment).where(Payment.tx_ref == tx_ref)
    payment = db.session.scalar(query)

    if not payment:
        raise Exception("tx_ref not found")

    if payment.get_status() in ("completed", "failed"):
        raise Exception("payment has already been resolved")

    if status == "success":
        payment.change_status("completed")
        db.session.commit()
        return True
    elif status == "failed":
        payment.change_status("failed")
        db.session.commit()
        return False

    return None
