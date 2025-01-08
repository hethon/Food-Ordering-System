import os

from dotenv import load_dotenv
import sqlalchemy as sa

from app.models import MenuItem, User
from app import db, app

load_dotenv()
app.app_context().push()


def add_mock_menu():
    menu_items = [
        {
            "id": 1,
            "name": "በየአይነት",
            "price": 75,
            "is_available": False,
        },
        {
            "id": 2,
            "name": "ሽሮ",
            "price": 50,
            "is_available": False,
        },
        {
            "id": 3,
            "name": "ምስር",
            "price": 55.00,
            "is_available": True,
        },
        {
            "id": 4,
            "name": "ድንች",
            "price": 50,
            "is_available": False,
        },
        {
            "id": 5,
            "name": "ፓስታ",
            "price": 55,
            "is_available": True,
        },
        {
            "id": 6,
            "name": "መኮረኒ",
            "price": 55,
            "is_available": True,
        },
        {
            "id": 7,
            "name": "ጎመን",
            "price": 45,
            "is_available": True,
        },
        {
            "id": 8,
            "name": "ፍርፍር",
            "price": 40,
            "is_available": True,
        },
        {
            "id": 9,
            "name": "ሩዝ",
            "price": 35,
            "is_available": True,
        },
        {
            "id": 10,
            "name": "እርጥብ",
            "price": 40,
            "is_available": True,
        },
    ]

    for item in menu_items:
        db.session.add(
            MenuItem(
                id=item["id"],
                name=item["name"],
                price=item["price"],
                is_available=item["is_available"],
            )
        )

    db.session.commit()


def add_admin_account():
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    PASS = os.getenv("ADMIN_PASS")

    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user:
        print("Admin account has already been added")
        return
    user = User(username=username, email=email, role="admin")
    user.set_password(PASS)
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    add_mock_menu()
    add_admin_account()
