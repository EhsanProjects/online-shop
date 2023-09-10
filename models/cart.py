from sqlalchemy import *
from sqlalchemy.orm import backref

from extensions import db


class Cart(db.Model):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref=backref('carts', lazy='dynamic'))

    def total_price(self):
        total = 0
        for item in self.cart_items:
            t = item.price * item.quantity
            total += t
        return total

    # name = Column(String, unique=True, nullable=False, index=True)
    # description = Column(String, nullable=False, index=True)
    # price = Column(Integer, nullable=False, index=True)
    # active = Column(Integer, nullable=False, index=True)
