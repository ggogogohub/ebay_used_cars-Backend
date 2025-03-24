from flask import request, jsonify, make_response
import jwt
from functools import wraps
import globals

# Use the existing MongoDB connection from globals
blacklist = globals.db.blacklist
users = globals.db.users
SECRET_KEY = globals.SECRET_KEY  # Use SECRET_KEY from globals.py

# JWT token required decorator
def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'error': 'Token is missing'}), 401)
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'error': 'Token has expired'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'error': 'Token is invalid'}), 401)

        bl_token = blacklist.find_one({'token': token})
        if bl_token is not None:
            return make_response(jsonify({'error': 'Token is blacklisted'}), 401)

        current_user = users.find_one({'username': data['user']})
        if not current_user:
            return make_response(jsonify({'error': 'User not found'}), 401)

        return func(current_user, *args, **kwargs)  # Pass current_user to the wrapped function
    return jwt_required_wrapper

def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(current_user, *args, **kwargs):
        if not current_user.get('role') == 'admin':  # Fixed admin role check
            return make_response(jsonify({'error': 'Admin access required'}), 403)

        return func(current_user, *args, **kwargs)

    return jwt_required(admin_required_wrapper)  # Ensuring jwt_required is applied
