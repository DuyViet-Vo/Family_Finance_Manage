from flask import Blueprint, request, jsonify
from models import db
from models.user import User

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Lấy danh sách tất cả người dùng.
    ---
    responses:
      200:
        description: Danh sách tất cả người dùng.
    """
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'username': user.username, 'email': user.email}
        output.append(user_data)
    return jsonify({'users': output})

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Lấy thông tin của một người dùng dựa trên ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Thông tin của người dùng.
    """
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Tạo mới một người dùng.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: User
          required:
            - username
            - email
          properties:
            username:
              type: string
              description: Tên người dùng.
            email:
              type: string
              description: Địa chỉ email của người dùng.
    responses:
      200:
        description: Người dùng đã được tạo thành công.
    """
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Cập nhật thông tin của một người dùng.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Tên người dùng.
            email:
              type: string
              description: Địa chỉ email.
    responses:
      200:
        description: Người dùng đã được cập nhật thành công.
    """
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Xóa một người dùng.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Người dùng đã được xóa thành công.
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})

