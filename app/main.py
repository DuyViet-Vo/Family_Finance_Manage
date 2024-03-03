from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vdv1810@localhost/test'
db = SQLAlchemy(app)

# Khai báo Swagger
swagger = Swagger(app)

class User(db.Model):
    __tablename__ = 'users'  # Định danh tên bảng là "users" thay vì "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.description}', '{self.price}')"

    
with app.app_context():
    db.create_all()

# users
@app.route('/users', methods=['GET'])
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

@app.route('/users/<int:user_id>', methods=['GET'])
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

@app.route('/users', methods=['POST'])
def create_user():
    """
    Tạo mới một người dùng.
    ---
    parameters:
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
        description: Người dùng đã được tạo thành công.
    """
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

@app.route('/users/<int:user_id>', methods=['PUT'])
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

@app.route('/users/<int:user_id>', methods=['DELETE'])
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

# products
@app.route('/products', methods=['GET'])
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
        product_data = {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price}
        output.append(product_data)
    return jsonify({'products': output})

@app.route('/products/<int:product_id>', methods=['GET'])
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
    return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price})

@app.route('/products', methods=['POST'])
def create_product():
    """
    Tạo mới một sản phẩm.
    ---
    parameters:
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
        description: Sản phẩm đã được tạo thành công.
    """
    data = request.json
    new_product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully!'})

@app.route('/products/<int:product_id>', methods=['PUT'])
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
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully!'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
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
    return jsonify({'message': 'Product deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)