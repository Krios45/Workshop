# Workshop Management

Ứng dụng web Django hỗ trợ quản lý xưởng, bao gồm tài sản, lịch đặt thiết bị, bảo trì, vật tư kho và tài khoản người dùng.

Demo: https://workshop-management-f0r7.onrender.com

## Chức năng chính

- Quản lý danh mục và thông tin tài sản trong xưởng.
- Tạo, duyệt, hủy và hoàn tất lịch đặt/mượn thiết bị.
- Theo dõi lịch bảo trì và trạng thái thiết bị.
- Quản lý vật tư, số lượng tồn kho và lịch sử nhập/xuất.
- Đăng ký, đăng nhập và cập nhật hồ sơ người dùng.
- Trang dashboard tổng quan và phân tích dữ liệu.

## Công nghệ sử dụng

- Python
- Django
- SQLite
- HTML, CSS, JavaScript
- WhiteNoise để phục vụ static files khi triển khai

## Cài đặt và chạy local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Mở trình duyệt tại:

- Ứng dụng: http://127.0.0.1:8000/
- Trang quản trị: http://127.0.0.1:8000/admin/

## Cấu trúc chính

- `accounts`: quản lý đăng nhập, đăng ký và hồ sơ người dùng.
- `assets`: quản lý tài sản và bảo trì.
- `bookings`: quản lý lịch đặt/mượn thiết bị.
- `inventory`: quản lý vật tư và giao dịch kho.
- `dashboard`: trang chủ, dashboard, thống kê và lịch bảo trì.

## Triển khai

Dự án có thể triển khai trên Render bằng `build.sh`. Khi deploy, cần cấu hình các biến môi trường như `SECRET_KEY`, `DEBUG` và `ALLOWED_HOSTS` nếu chạy ở môi trường production.
