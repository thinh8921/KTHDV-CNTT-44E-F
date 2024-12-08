from flask import Blueprint, jsonify, request
from models import Order, db
from middleware.token_validation import token_required

order_routes = Blueprint('orders', __name__)

@order_routes.route('/orders', methods=['GET'])
@token_required
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'customer_name': order.customer_name,
        'customer_email': order.customer_email,
        'total_amount': float(order.total_amount),
        'status': order.status,
        'created_at': order.created_at,
        'updated_at': order.updated_at
    } for order in orders])

@order_routes.route('/orders/<int:id>', methods=['GET'])
@token_required
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify(message="Order not found"), 404

    return jsonify({
        'id': order.id,
        'customer_name': order.customer_name,
        'customer_email': order.customer_email,
        'total_amount': float(order.total_amount),
        'status': order.status,
        'created_at': order.created_at,
        'updated_at': order.updated_at
    })

@order_routes.route('/orders', methods=['POST'])
@token_required
def create_order():
    data = request.get_json()
    new_order = Order(
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        total_amount=data['total_amount'],
        status=data.get('status', 'pending')
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(message="Order created successfully", order_id=new_order.id), 201

@order_routes.route('/orders/<int:id>', methods=['PUT'])
@token_required
def update_order(id):
    data = request.get_json()
    order = Order.query.get(id)
    if not order:
        return jsonify(message="Order not found"), 404

    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify(message="Order updated successfully"), 200

@order_routes.route('/orders/<int:id>', methods=['DELETE'])
@token_required
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify(message="Order not found"), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify(message="Order deleted successfully"), 200
