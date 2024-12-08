from flask import Blueprint, jsonify, request
from models import OrderReport, ProductReport, db
from middleware.token_validation import token_required
import requests

report_routes = Blueprint('reports', __name__)

@report_routes.route('/reports/products', methods=['GET'])
@token_required
def get_product_reports():
    reports = ProductReport.query.all()
    return jsonify([{
        'id': report.id,
        'order_report_id': report.order_report_id,
        'product_id': report.product_id,
        'total_sold': report.total_sold,
        'revenue': float(report.revenue),
        'cost': float(report.cost),
        'profit': float(report.profit),
        'created_at': report.created_at
    } for report in reports])

@report_routes.route('/reports/products/<int:id>', methods=['GET'])
@token_required
def get_product_report(id):
    report = ProductReport.query.get(id)
    if not report:
        return jsonify(message="Product report not found"), 404

    return jsonify({
        'id': report.id,
        'order_report_id': report.order_report_id,
        'product_id': report.product_id,
        'total_sold': report.total_sold,
        'revenue': float(report.revenue),
        'cost': float(report.cost),
        'profit': float(report.profit),
        'created_at': report.created_at
    })

@report_routes.route('/reports/orders', methods=['GET'])
@token_required
def get_order_reports():
    reports = OrderReport.query.all()
    return jsonify([{
        'id': report.id,
        'order_id': report.order_id,
        'total_revenue': float(report.total_revenue),
        'total_cost': float(report.total_cost),
        'total_profit': float(report.total_profit),
        'created_at': report.created_at
    } for report in reports])

@report_routes.route('/reports/orders/<int:id>', methods=['GET'])
@token_required
def get_order_report(id):
    report = OrderReport.query.get(id)
    if not report:
        return jsonify(message="Order report not found"), 404

    return jsonify({
        'id': report.id,
        'order_id': report.order_id,
        'total_revenue': float(report.total_revenue),
        'total_cost': float(report.total_cost),
        'total_profit': float(report.total_profit),
        'created_at': report.created_at
    })

@report_routes.route('/reports/products', methods=['POST'])
@token_required
def create_product_report():
    data = request.get_json()
    # Call external services to fetch data
    # Example: Fetch product and order data via requests
    # Update calculation logic here
    new_report = ProductReport(
        order_report_id=data['order_report_id'],
        product_id=data['product_id'],
        total_sold=data['total_sold'],
        revenue=data['revenue'],
        cost=data['cost'],
        profit=data['profit']
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify(message="Product report created successfully"), 201

