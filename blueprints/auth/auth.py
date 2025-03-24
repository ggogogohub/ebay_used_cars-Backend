from flask import Blueprint, request, jsonify, make_response
from decorators import jwt_required
import jwt
import datetime
import bcrypt
import globals


auth_bp = Blueprint('auth_bp', __name__)

blacklist = globals.db.blacklist
users = globals.db.users
SECRET_KEY = globals.SECRET_KEY

# User Registration
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "buyer")  # Default role is "buyer"

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed_pw, "role": role})
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@auth_bp.route('/auth/login', methods=['GET'])
def login():
    auth = request.authorization

    # Ensure authentication headers are provided
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({'message': 'Missing authentication credentials'}), 401)

    # Find user in the database
    user = users.find_one({'username': auth.username})
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    # Verify password
    if not bcrypt.checkpw(auth.password.encode('utf-8'), user['password']):
        return make_response(jsonify({'message': 'Invalid password'}), 401)

    # Generate JWT token
    token = jwt.encode({
        'user': auth.username,
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token valid for 1 hour
    }, globals.SECRET_KEY, algorithm='HS256')

    return make_response(jsonify({'token': token}), 200)


# Get User Profile
@auth_bp.route('/auth/profile', methods=['GET'])
@jwt_required
def profile(current_user):
    return jsonify({"username": current_user["username"], "role": current_user["role"]}), 200

# User Account Deletion
@auth_bp.route('/auth/delete', methods=['DELETE'])
@jwt_required
def delete_account(current_user):
    users.delete_one({"username": current_user["username"]})
    return jsonify({"message": "User account deleted"}), 200

# User Logout
@auth_bp.route('/auth/logout', methods=['GET'])
@jwt_required
def logout(current_user):
    token = request.headers.get('x-access-token')
    if not token:
        return jsonify({"error": "Token missing"}), 400

    blacklist.insert_one({'token': token})
    return make_response(jsonify({'message': 'Logged out successfully'}), 200)
