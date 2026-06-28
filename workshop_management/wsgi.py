"""
WSGI config for workshop_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workshop_management.settings')

application = get_wsgi_application()

# Tự động chạy migrate khi server khởi động (để phòng trường hợp chủ repo chưa cấu hình build.sh)
try:
    from django.core.management import call_command
    print("Running automatic startup migrations...")
    call_command('migrate', interactive=False)
    print("Automatic startup migrations completed successfully.")
except Exception as e:
    print("Failed to run startup migrations:", e)
