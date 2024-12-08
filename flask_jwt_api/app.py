from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes.auth_routes import auth_routes
from routes.hello_routes import hello_routes

app = Flask(__name__)

# Cấu hình ứng dụng
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Thay bằng secret key thực tế

# Khởi tạo các thành phần
db.init_app(app)
jwt = JWTManager(app)

# Đăng ký các blueprint (Router)
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(hello_routes, url_prefix='/')

# Tạo bảng dữ liệu
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8001)
