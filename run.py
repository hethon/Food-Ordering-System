from dotenv import load_dotenv

load_dotenv()

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, MenuItem, Order, OrderItem, Payment


@app.shell_context_processor
def make_shell_context():
    return {
        "sa": sa,
        "so": so,
        "db": db,
        "User": User,
        "MenuItem": MenuItem,
        "Order": Order,
        "OrderItem": OrderItem,
        "Payment": Payment,
    }
