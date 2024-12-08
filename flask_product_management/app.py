from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db
from routes.product_routes import product_routes

app = Flask(__name__)

# Cấu hình ứng dụng
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

# Khởi tạo các thành phần
db.init_app(app)
jwt = JWTManager(app)

# Đăng ký blueprint
app.register_blueprint(product_routes, url_prefix='/')

# Tạo bảng dữ liệu
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8001)
