from flask import Blueprint, jsonify
from middleware.token_validation import token_required

hello_routes = Blueprint('hello', __name__)

@hello_routes.route('/hello', methods=['GET'])
@token_required
def hello_world():
    return jsonify(message="Hello, World!"), 200
