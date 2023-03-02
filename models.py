from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Double
from sqlalchemy.orm import validates

from app import db


class SaleOrder(db.Model):
    __tablename__ = 'saleorder'
    id = Column(Integer, primary_key=True)
    order_number = Column(String(50))
    customer = Column(String(50))
    order_date = Column(DateTime)
    total_amount = Column(Double)

    def __str__(self):
        return self.ordernumber

class SaleOrderItem(db.Model):
    __tablename__ = 'saleorderitem'
    id = Column(Integer, primary_key=True)
    saleorder = Column(Integer, ForeignKey('saleorder.id', ondelete="CASCADE"))
    product = Column(String(30))
    quantity = Column(Integer)
    item_description = Column(String(500))
    creation_date = Column(DateTime)
    subtotal = Column(Double)

    @validates('rating')
    def validate_quantity(self, key, value):
        assert value is None or (1 <= value <= 10)
        return value

    def __str__(self):
        return f"{self.product}: {self.creation_date:%x}"
