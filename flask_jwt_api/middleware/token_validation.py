from flask_jwt_extended import verify_jwt_in_request
from flask import jsonify

def token_required(f):
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify(message="Token validation failed"), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
