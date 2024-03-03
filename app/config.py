import os

# Cấu hình SQLALCHEMY_DATABASE_URI
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://postgres:vdv1810@localhost/test'

# Cấu hình cho các ứng dụng khác nếu cần
# ...

# Cấu hình Swagger
SWAGGER = {
    'title': 'Your API title',
    'uiversion': 3
}
