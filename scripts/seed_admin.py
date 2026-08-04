from sqlalchemy import select

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import User, UserRole


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.scalar(select(User).where(User.username == settings.admin_username))
        if existing is None:
            db.add(
                User(
                    full_name="مدیر سیستم",
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                    role=UserRole.admin,
                    must_change_password=True,
                )
            )
            db.commit()
            print(f"Created admin user: {settings.admin_username}")
        else:
            print(f"Admin user already exists: {settings.admin_username}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
