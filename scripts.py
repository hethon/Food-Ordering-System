import os

from app.models import MenuItem, User
from app import db, app


app.app_context().push()


def add_mock_menu():
    menu_items = [
        {
            "id": 1,
            "name": "Waffle with Berries",
            "price": 6.50,
            "is_available": False,
        },
        {
            "id": 2,
            "name": "Vanilla Bean Crème Brûlée",
            "price": 7.00,
            "is_available": False,
        },
        {
            "id": 3,
            "name": "Macaron Mix of Five",
            "price": 8.00,
            "is_available": True,
        },
        {
            "id": 4,
            "name": "Classic Tiramisu",
            "price": 5.50,
            "is_available": False,
        },
        {
            "id": 5,
            "name": "Pistachio Baklava",
            "price": 4.00,
            "is_available": True,
        },
        {
            "id": 6,
            "name": "Lemon Meringue Pie",
            "price": 5.00,
            "is_available": True,
        },
        {
            "id": 7,
            "name": "Red Velvet Cake",
            "price": 4.50,
            "is_available": True,
        },
        {
            "id": 8,
            "name": "Salted Caramel Brownie",
            "price": 4.50,
            "is_available": True,
        },
        {
            "id": 9,
            "name": "Vanilla Panna Cotta",
            "price": 6.50,
            "is_available": True,
        },
    ]

    for item in menu_items:
        db.session.add(
            MenuItem(
                name=item["name"],
                price=item["price"],
                is_available=item["is_available"],
            )
        )

    db.session.commit()


def add_admin_account():
    user = User(username="admin", email="admin@fos.com", role="admin")
    user.set_password(os.getenv("ADMIN_PASS"))
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    # add_mock_menu()
    pass
