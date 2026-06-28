#!/usr/bin/env bash
# Build script chạy trên Render mỗi lần deploy

set -o errexit   # dừng nếu có lỗi

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_data

# Tạo superuser admin nếu chưa có
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser admin created.')
else:
    print('Superuser admin already exists.')
"
