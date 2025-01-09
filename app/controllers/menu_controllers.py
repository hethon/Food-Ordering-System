import sqlalchemy as sa

from app import db
from app.models import MenuItem, Order


def get_menu_items():
    query = sa.select(MenuItem)
    return db.session.scalars(query)


def all_menu_items_available(menu_items):
    for menu_item in menu_items:
        if not menu_item.is_available:
            return False
    return True


def _get_order_items(order):
    query = order.order_items.select()
    db.session.scalars(query).all()


class _Order:
    """wrapper around order to bind order items with it"""

    def __init__(self, order):
        self.order = order

    def __getattr__(self, name):
        return getattr(self.order, name)

    @property
    def order_items(self):
        query = self.order.order_items.select()
        return db.session.scalars(query).all()


def get_active_orders():
    """return orders with completed payment"""

    query = sa.select(Order).where(Order.status == "pending")
    for order in db.session.scalars(query):
        # the payment associated with the order
        payment = db.session.scalar(order.payment.select())
        if payment.get_status() == "completed":
            # yield only if the payment is completed
            yield _Order(order)


def set_menu_item_availability(menu_item_id, new_state):
    menu_item = db.session.get(MenuItem, menu_item_id)
    if not menu_item:
        raise Exception("menu item doesn't exist.")

    if menu_item.is_available == new_state:
        raise Exception(
            f"menu_item is already {'available' if new_state else 'unavailable'}"
        )

    menu_item.toggle_availability()
    db.session.commit()
