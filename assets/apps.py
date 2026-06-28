from django.apps import AppConfig


class AssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assets'

    def ready(self):
        import sys
        # Do not run when creating/checking migrations locally
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            try:
                from django.core.management import call_command
                print("Django AssetsConfig startup: Running migrations...")
                call_command('migrate', interactive=False)
                print("Django AssetsConfig startup: Migrations run completed.")
            except Exception as e:
                print("Django AssetsConfig startup: Migration failed:", e)
