from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import db, User, Product, Order, OrderItem, OrderReport, ProductReport
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo DB và JWT
db.init_app(app)
jwt = JWTManager(app)

# Tạo bảng nếu chưa tồn tại
with app.app_context():
    db.create_all()

# ĐN và tạo Jwt
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('userName')
    password = request.json.get('password')
    user = User.query.filter_by(UserName=username).first()
    if user and user.Password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

# báo cáo sp
@app.route('/reports/products', methods=['GET'])
@jwt_required()
def get_product_reports():
    reports = ProductReport.query.all()
    result = []
    for report in reports:
        result.append({
            'product_id': report.product_id,
            'total_sold': report.total_sold,
            'revenue': str(report.revenue),
            'cost': str(report.cost),
            'profit': str(report.profit)
        })
    return jsonify({"product_reports": result}), 200

# hiện sp
@app.route('/reports/products', methods=['POST'])
@jwt_required()
def create_product_report():
    data = request.get_json()
    product_id = data.get('product_id')
    total_sold = data.get('total_sold')
    revenue = data.get('revenue')
    cost = data.get('cost')
    profit = data.get('profit')
    
    new_report = ProductReport(product_id=product_id, total_sold=total_sold, revenue=revenue, cost=cost, profit=profit)
    db.session.add(new_report)
    db.session.commit()
    return jsonify(message="Product report created", report_id=new_report.id), 201

# hiện đơn hàng
@app.route('/reports/orders', methods=['GET'])
@jwt_required()
def get_order_reports():
    reports = OrderReport.query.all()
    result = []
    for report in reports:
        result.append({
            'order_id': report.order_id,
            'total_revenue': str(report.total_revenue),
            'total_cost': str(report.total_cost),
            'total_profit': str(report.total_profit)
        })
    return jsonify({"order_reports": result}), 200

# tạo  đơn hàng
@app.route('/reports/orders', methods=['POST'])
@jwt_required()
def create_order_report():
    data = request.get_json()
    order_id = data.get('order_id')
    total_revenue = data.get('total_revenue')
    total_cost = data.get('total_cost')
    total_profit = data.get('total_profit')
    
    new_report = OrderReport(order_id=order_id, total_revenue=total_revenue, total_cost=total_cost, total_profit=total_profit)
    db.session.add(new_report)
    db.session.commit()
    return jsonify(message="Order report created", report_id=new_report.id), 201

#  Xóa sản phẩm
@app.route('/reports/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product_report(id):
    report = ProductReport.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    return jsonify(message="Product report deleted"), 200

#Xóa đơn
@app.route('/reports/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order_report(id):
    report = OrderReport.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    return jsonify(message="Order report deleted"), 200

if __name__ == '__main__':
    app.run(debug=True, port=6005)
