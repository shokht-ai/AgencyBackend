import os
import shutil
import django
from django.core.management import call_command

# PROJECT ROOT (manage.py joylashgan papka)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {"__pycache__"}


def clean_migrations(app_path):
    """migrations papkasini tozalaydi"""
    migrations_path = os.path.join(app_path, "migrations")

    if not os.path.exists(migrations_path):
        return

    print(f"[CLEANING] {migrations_path}")

    for file in os.listdir(migrations_path):
        full_path = os.path.join(migrations_path, file)

        # __init__.py qolsin
        if file == "__init__.py":
            continue

        # pycache
        if file in EXCLUDE:
            shutil.rmtree(full_path, ignore_errors=True)
            continue

        # fayl yoki papkani o‘chirish
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path, ignore_errors=True)

    print("[DONE] migrations cleaned.\n")


def find_apps():
    """project ichidagi app-larni topish"""
    apps = []
    for item in os.listdir(PROJECT_DIR):
        full_path = os.path.join(PROJECT_DIR, item)

        if os.path.isdir(full_path):
            if os.path.exists(os.path.join(full_path, "migrations")):
                apps.append(full_path)

    return apps


def delete_sqlite():
    """database-ni o‘chirish"""
    db_path = os.path.join(PROJECT_DIR, "db.sqlite3")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("[DB DELETED] db.sqlite3 o‘chirildi.\n")
    else:
        print("[INFO] db.sqlite3 topilmadi.\n")


def django_setup():
    """django init"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agencybackend.settings")
    # ❗ settings modul nomini project bo‘yicha o‘zgartiring
    django.setup()


def create_users():
    """superuser va oddiy user yaratish"""
    from django.contrib.auth.models import User

    # Superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        print("[SUPERUSER CREATED] admin / admin123")

    # Oddiy user
    if not User.objects.filter(username="user").exists():
        User.objects.create_user(
            username="user",
            email="user@example.com",
            password="user123"
        )
        print("[USER CREATED] user / user123")


def main():
    print("\n========== Django Migration Cleaner ==========\n")

    # 1) migrations tozalash
    apps = find_apps()
    for app in apps:
        clean_migrations(app)

    # 2) db.sqlite3 o‘chirish
    delete_sqlite()

    # 3) django setup
    django_setup()

    # 4) makemigrations + migrate
    print("[MIGRATING...]")
    call_command("makemigrations")
    call_command("migrate")
    print("[DONE] migrations yaratildi.\n")

    # 5) default foydalanuvchilarni yaratish
    create_users()

    print("\n===== HAMMASI MUVAFFAQIYATLI BAJARILDI! =====\n")


if __name__ == "__main__":
    main()
