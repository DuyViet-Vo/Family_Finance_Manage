# setting.py

SWAGGER_SETTINGS = {
    "title": "VIET",
    "uiversion": 3,  # Sử dụng phiên bản UI Swagger 3 (thay đổi tùy chọn)
    "specs_route": "/api/docs/",  # Đường dẫn tới tài liệu Swagger
    "static_url_path": "/api/docs/swaggerui/",
    "swagger_ui": True,  # Bật hoặc tắt giao diện người dùng Swagger UI
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",  # Đường dẫn tới tệp mô tả JSON
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "securityDefinitions": {"BasicAuth": {"type": "basic"}},
    "security": [{"BasicAuth": []}],
    "route": {
        "url": "/api/docs/swagger.json",  # Đường dẫn tới tệp mô tả JSON
        "spec": {"info": {"title": "API documentation"}},  # Thông tin về API
    },
    "template": {
        "swagger": "index.html",  # Mẫu HTML tùy chỉnh cho Swagger UI
        "schemes": ["http", "https"],  # Các giao thức cho API (HTTP, HTTPS)
        "tags_sorter": "alpha",  # Sắp xếp thẻ theo thứ tự chữ cái
        "operations_sorter": "alpha",  # Sắp xếp hoạt động theo thứ tự chữ cái
    },
}

SQLALCHEMY_DATABASE_URI = (
    "postgresql://postgres:vdv1810@localhost/finance_manage"  # noqa
)
SECRET_KEY = "duyvietvo"
