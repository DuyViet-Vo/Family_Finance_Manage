import hashlib
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, request

from config.settings import SECRET_KEY
from models import db
from models.user import User

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
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
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        output.append(user_data)
    return jsonify({"users": output})


@user_bp.route("/users/<int:user_id>", methods=["GET"])
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
    return jsonify(
        {"id": user.id, "username": user.username, "email": user.email}
    )


# Đăng ký người dùng
@user_bp.route("/register", methods=["POST"])
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

    if User.query.filter_by(email=data["email"]).first() is not None:
        return jsonify({"message": "Email already exists"}), 400
    if User.query.filter_by(username=data["username"]).first() is not None:
        return jsonify({"message": "Username already exists"}), 400
    # Mã hoá mật khẩu thành MD5
    password = data["password"]
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    new_user = User(
        username=data["username"],
        password=hashed_password,
        email=data["email"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    """
    Người dùng đăng nhập.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: User
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: Địa chỉ email của người dùng.
            password:
              type: string
              description: Mật khẩu người dùng
    responses:
      200:
        description: Người dùng đăng nhập thành công.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or user.password != hashlib.md5(password.encode()).hexdigest():
        return jsonify({"message": "Invalid email or password"}), 401

    # Create access token
    access_token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(minutes=60)},
        SECRET_KEY,
    )

    # Create refresh token
    refresh_token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY,
    )

    return (
        jsonify(
            {"access_token": access_token, "refresh_token": refresh_token}
        ),
        200,
    )
