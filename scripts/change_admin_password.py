import getpass

from sqlalchemy import select

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import User


def main() -> None:
    username = input(f"Admin username [{settings.admin_username}]: ").strip() or settings.admin_username
    password = getpass.getpass("New password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        raise SystemExit("Passwords do not match")
    if len(password) < 8:
        raise SystemExit("Password must be at least 8 characters")
    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.username == username))
        if user is None:
            raise SystemExit("User not found")
        user.password_hash = hash_password(password)
        user.must_change_password = False
        db.commit()
        print("Password changed")
    finally:
        db.close()


if __name__ == "__main__":
    main()
