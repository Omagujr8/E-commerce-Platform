from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem


def create_order(db: Session, order: Order, items: list[OrderItem]):
    db.add(order)
    db.flush()

    for item in items:
        item.order_id = order.id
        db.add(item)

    db.commit()
    db.refresh(order)

    return order


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()