from flask import Blueprint, jsonify, request

from models import db
from models.product import Product

product_bp = Blueprint("products", __name__)


@product_bp.route("/products", methods=["GET"])
def get_products():
    """
    Lấy danh sách tất cả sản phẩm.
    ---
    responses:
      200:
        description: Danh sách tất cả sản phẩm.
    """
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
        output.append(product_data)
    return jsonify({"products": output})


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Lấy thông tin của một sản phẩm dựa trên ID.
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Thông tin của sản phẩm.
    """
    product = Product.query.get_or_404(product_id)
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
    )


@product_bp.route("/products", methods=["POST"])
def create_product():
    """
    Tạo mới một sản phẩm.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Product
          required:
            - name
            - description
            - price
          properties:
            name:
              type: string
              description: Tên sản phẩm.
            description:
              type: string
              description: Mô tả sản phẩm.
            price:
              type: number
              description: Giá của sản phẩm.
    responses:
      200:
        description: Sản phẩm đã được tạo thành công.
    """
    data = request.json
    new_product = Product(
        name=data["name"], description=data["description"], price=data["price"]
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully!"})


@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Cập nhật thông tin của một sản phẩm.
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Tên sản phẩm.
            description:
              type: string
              description: Mô tả sản phẩm.
            price:
              type: number
              description: Giá sản phẩm.
    responses:
      200:
        description: Sản phẩm đã được cập nhật thành công.
    """
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data["name"]
    product.description = data["description"]
    product.price = data["price"]
    db.session.commit()
    return jsonify({"message": "Product updated successfully!"})


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Xóa một sản phẩm.
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Sản phẩm đã được xóa thành công.
    """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})
