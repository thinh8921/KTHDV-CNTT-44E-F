from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class OrderReport(db.Model):
    __tablename__ = 'orders_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    total_profit = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product_reports = db.relationship('ProductReport', backref='order_report', cascade="all, delete-orphan")


class ProductReport(db.Model):
    __tablename__ = 'product_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_report_id = db.Column(db.Integer, db.ForeignKey('orders_reports.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    total_sold = db.Column(db.Integer, nullable=False, default=0)
    revenue = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    cost = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    profit = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

