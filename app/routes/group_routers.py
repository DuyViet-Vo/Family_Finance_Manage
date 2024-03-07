from flask import Blueprint, jsonify, request

from models import db
from models.group import Group

group_db = Blueprint("groups", __name__)


@group_db.route("/groups", methods=["GET"])
def get_groups():
    """
    Lấy danh sách tất cả nhóm với thông tin người tạo nhóm.
    ---
    responses:
      200:
        description: Danh sách tất cả nhóm với thông tin người tạo nhóm.
    """
    groups = Group.query.all()
    output = []
    for group in groups:
        group_data = {
            "id": group.id,
            "group_name": group.group_name,
            "user_create": {
                "id": group.creator.id,
                "username": group.creator.username,
                "email": group.creator.email,
            },
            "created_at": group.created_at,
        }
        output.append(group_data)
    return jsonify({"groups": output})


@group_db.route("/groups/<int:group_id>", methods=["GET"])
def get_group(group_id):
    """
    Lấy thông tin của một nhóm dựa trên ID với thông tin người tạo nhóm.
    ---
    parameters:
      - name: group_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Thông tin của nhóm với thông tin người tạo nhóm.
    """
    group = Group.query.get_or_404(group_id)
    group_data = {
        "id": group.id,
        "group_name": group.group_name,
        "user_create": {
            "id": group.creator.id,
            "username": group.creator.username,
            "email": group.creator.email,
        },
        "created_at": group.created_at,
    }
    return jsonify(group_data)


@group_db.route("/groups", methods=["POST"])
def create_group():
    """
    Tạo mới một nhóm.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Group
          required:
            - group_name
            - user_create
          properties:
            group_name:
              type: string
              description: Tên nhóm.
            user_create:
              type: integer
              description: ID của người tạo nhóm.
    responses:
      200:
        description: Nhóm đã được tạo thành công.
    """
    data = request.json
    new_group = Group(
        group_name=data["group_name"], user_create=data["user_create"]
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group created successfully!"})


@group_db.route("/groups/<int:group_id>", methods=["PUT"])
def update_group(group_id):
    """
    Cập nhật thông tin của một nhóm.
    ---
    parameters:
      - name: group_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            group_name:
              type: string
              description: Tên nhóm.
    responses:
      200:
        description: Nhóm đã được cập nhật thành công.
    """
    group = Group.query.get_or_404(group_id)
    data = request.json
    group.group_name = data["group_name"]
    db.session.commit()
    return jsonify({"message": "Group updated successfully!"})


@group_db.route("/groups/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    """
    Xóa một nhóm.
    ---
    parameters:
      - name: group_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Nhóm đã được xóa thành công.
    """
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    return jsonify({"message": "Group deleted successfully!"})
