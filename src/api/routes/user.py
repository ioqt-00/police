from flask import Response, jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import db
from model import User
from routes.helpers import admin_required

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/users', methods=['GET'])
@admin_required()
def get_users() -> Response:
    """GET request to fetch all users"""
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@user_bp.route('/<int:user_id>', methods=['GET'])
@admin_required()
def get_user(user_id: int) -> Response:
    """GET request to fetch a specific user by id"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })


@user_bp.route('/', methods=['POST'])
def create_user() -> tuple[Response, int]:
    data = request.json
    username = data['username']
    user = User.query.filter(User.username == username).first()
    if user is not None:
        return jsonify({'message': f'User with username {username} already exists', 'id': user.id}), 403
    new_user = User(username=username, email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required()
def update_user(user_id: int) -> tuple[Response, int]:
    user = User.query.get_or_404(user_id)
    data = request.json

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user_client() -> tuple[Response, int]:
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.json

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required()
def delete_user(user_id: int) -> tuple[Response, int]:
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
