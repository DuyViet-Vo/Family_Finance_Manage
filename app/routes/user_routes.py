from flask import Blueprint, request, jsonify
from models import db
from models.user import User
from sqlalchemy.exc import IntegrityError

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

# Đăng ký người dùng
@user_bp.route('/register', methods=['POST'])
def register():
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
            - password
          properties:
            username:
              type: string
              description: Tên người dùng.
            email:
              type: string
              description: Địa chỉ email của người dùng.
            password:
              type: string
              description: Mật khẩu người dùng
    responses:
      200:
        description: Người dùng đã được tạo thành công.
    """
  data = request.get_json()
  new_user = User(username=data['username'], password=data['password'], email=data['email'])
  try:
      db.session.add(new_user)
      db.session.commit()
      return jsonify({'message': 'User created successfully'}), 201
  except IntegrityError:
      db.session.rollback()
      return jsonify({'message': 'Username or email already exists'}), 400



