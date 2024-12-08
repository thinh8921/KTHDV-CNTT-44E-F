from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
from models import User, db

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('userName')
    password = data.get('password')

    user = User.query.filter_by(UserName=username).first()
    if user and check_password_hash(user.Password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify(message="Invalid credentials"), 401
