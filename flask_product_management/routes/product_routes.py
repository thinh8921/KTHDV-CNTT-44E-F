from flask import Blueprint, jsonify, request
from models import Product, db
from middleware.token_validation import token_required

product_routes = Blueprint('products', __name__)

@product_routes.route('/products', methods=['GET'])
@token_required
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'quantity': product.quantity,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    } for product in products])

@product_routes.route('/products/<int:id>', methods=['GET'])
@token_required
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify(message="Product not found"), 404

    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'quantity': product.quantity,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    })

@product_routes.route('/products', methods=['POST'])
@token_required
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(message="Product created successfully"), 201

@product_routes.route('/products/<int:id>', methods=['PUT'])
@token_required
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if not product:
        return jsonify(message="Product not found"), 404

    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.quantity = data['quantity']
    db.session.commit()
    return jsonify(message="Product updated successfully"), 200

@product_routes.route('/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify(message="Product not found"), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify(message="Product deleted successfully"), 200
