from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import json

import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class UserRole(Enum):
    customer = 1
    staff = 2
    admin = 3


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    role: so.Mapped[UserRole] = so.mapped_column(default=UserRole.customer)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    orders: so.WriteOnlyMapped["Order"] = so.relationship(back_populates="owner")
    payments: so.WriteOnlyMapped["Payment"] = so.relationship(back_populates="owner")

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        return self.role.name


class MenuItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    price: so.Mapped[float]
    is_available: so.Mapped[bool]

    order_items: so.WriteOnlyMapped["OrderItem"] = so.relationship(
        back_populates="menu_item"
    )

    def __repr__(self):
        return f"Menu('{self.id}', '{self.name}')"

    def as_json_string(self):
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "price": self.price,
                "is_available": self.is_available,
            },
            separators=(",", ":"),
        )

    def toggle_availability(self):
        self.is_available = not (self.is_available)


class OrderStatus(Enum):
    pending = 1
    completed = 2
    canceled = 3


class Order(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    total_price: so.Mapped[float]
    status: so.Mapped[OrderStatus]
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    owner: so.Mapped[User] = so.relationship(back_populates="orders")

    order_items: so.WriteOnlyMapped["OrderItem"] = so.relationship(
        back_populates="order"
    )
    payment: so.WriteOnlyMapped["Payment"] = so.relationship(back_populates="order")

    def __repr__(self):
        return f"Order('{self.id}', '{self.total_price}', '{self.user_id}')"

    def change_status(self, new_status):
        self.status = OrderStatus[new_status]


class OrderItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quantity: so.Mapped[int]
    price: so.Mapped[float]
    order_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Order.id), index=True)
    menu_item_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(MenuItem.id), index=True
    )

    menu_item: so.Mapped[MenuItem] = so.relationship(back_populates="order_items")
    order: so.Mapped[Order] = so.relationship(back_populates="order_items")

    def __repr__(self):
        return f"OrderItem('{self.id=}', '{self.order_id=}', '{self.menu_item_id=}')"


class PaymentStatus(Enum):
    pending = 1
    completed = 2
    failed = 3


class Payment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[float]
    status: so.Mapped[PaymentStatus]
    tx_ref: so.Mapped[str] = so.mapped_column(unique=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    order_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Order.id), index=True)

    owner: so.Mapped[User] = so.relationship(back_populates="payments")
    order: so.Mapped[Order] = so.relationship(back_populates="payment")

    def __repr__(self):
        return f"Payment('{self.id}', '{self.amount}', '{self.tx_ref}')"

    def change_status(self, new_status):
        self.status = PaymentStatus[new_status]

    def get_status(self):
        return self.status.name


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
