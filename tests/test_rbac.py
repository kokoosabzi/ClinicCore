from app.core.security import hash_password, verify_password
from app.models.role import Permission, Role, RolePermission
from app.models.user import User, UserRole


ROLE_LABELS = {
    "admin": "مدیر سیستم",
    "clinic_manager": "مدیر کلینیک",
    "doctor": "پزشک",
    "secretary": "پذیرش",
    "accountant": "حسابدار",
}


def seed_rbac(db_session):
    roles = {}
    for key, label in ROLE_LABELS.items():
        role = Role(key=key, label=label, is_system=True, is_active=True)
        db_session.add(role)
        roles[key] = role
    codes = [
        "users.view", "users.create", "users.update", "users.deactivate",
        "users.reset_password", "users.assign_role", "roles.manage",
        "patients.view", "patients.create", "patients.update", "patients.archive",
        "appointments.view", "appointments.create", "appointments.update", "appointments.cancel",
        "financial.view", "financial.create", "financial.update", "financial.void",
        "messaging.view", "messaging.create", "reports.view", "reports.financial",
        "settings.view", "settings.update", "audit.view",
    ]
    db_session.add_all(
        Permission(code=code, label=code, category=code.split(".", 1)[0])
        for code in codes
    )
    db_session.flush()
    grants = {
        "admin": codes,
        "clinic_manager": [
            code for code in codes
            if code not in {"users.assign_role", "roles.manage", "settings.view", "settings.update"}
        ],
        "doctor": [
            "patients.view", "patients.create", "patients.update",
            "appointments.view", "appointments.create", "appointments.update", "appointments.cancel",
            "messaging.view", "messaging.create",
        ],
        "secretary": [
            "patients.view", "patients.create", "patients.update",
            "appointments.view", "appointments.create", "appointments.update", "appointments.cancel",
            "messaging.view", "messaging.create",
        ],
        "accountant": [
            "patients.view", "financial.view", "financial.create", "financial.update", "reports.financial",
        ],
    }
    for role_key, permission_codes in grants.items():
        db_session.add_all(
            RolePermission(role_id=roles[role_key].id, permission_code=code)
            for code in permission_codes
        )
    db_session.commit()


def login(client, username, password="test-password-123"):
    return client.post("/login", data={"username": username, "password": password})


def test_doctor_has_patient_access_but_not_financial_access(client, db_session):
    seed_rbac(db_session)
    db_session.add(
        User(
            full_name="پزشک آزمایشی",
            username="doctor1",
            password_hash=hash_password("test-password-123"),
            role=UserRole.doctor,
            must_change_password=False,
        )
    )
    db_session.commit()

    response = login(client, "doctor1")
    assert response.status_code == 200
    assert client.get("/patients").status_code == 200
    assert client.get("/financial").status_code == 403
    assert client.get("/users/manage").status_code == 403


def test_admin_can_create_user_from_management_page(client, db_session):
    seed_rbac(db_session)
    db_session.add(
        User(
            full_name="مدیر",
            username="rootadmin",
            password_hash=hash_password("test-password-123"),
            role=UserRole.admin,
            must_change_password=False,
        )
    )
    db_session.commit()

    assert login(client, "rootadmin").status_code == 200
    page = client.get("/users/manage")
    assert page.status_code == 200
    import re
    csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', page.text).group(1)

    response = client.post(
        "/users/ui/create",
        data={
            "csrf_token": csrf_token,
            "full_name": "کارمند جدید",
            "username": "staff.new",
            "password": "new-password-123",
            "role": "doctor",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    created = db_session.query(User).filter_by(username="staff.new").one()
    assert created.role == UserRole.doctor
    assert created.must_change_password is True
    assert verify_password("new-password-123", created.password_hash)
    assert "new-password-123" not in created.password_hash


def test_clinic_manager_cannot_assign_roles_or_manage_admin(client, db_session):
    seed_rbac(db_session)
    db_session.add_all(
        [
            User(
                full_name="مدیر کلینیک",
                username="manager1",
                password_hash=hash_password("test-password-123"),
                role=UserRole.clinic_manager,
                must_change_password=False,
            ),
            User(
                full_name="مدیر سیستم",
                username="systemadmin",
                password_hash=hash_password("test-password-123"),
                role=UserRole.admin,
                must_change_password=False,
            ),
        ]
    )
    db_session.commit()

    assert login(client, "manager1").status_code == 200
    denied = client.post(
        "/users/",
        json={
            "full_name": "پزشک جدید",
            "username": "doctor.new",
            "password": "new-password-123",
            "role": "doctor",
        },
    )
    assert denied.status_code == 403


def test_forced_password_change_blocks_dashboard(client, db_session):
    seed_rbac(db_session)
    db_session.add(
        User(
            full_name="کاربر تازه",
            username="new.user",
            password_hash=hash_password("test-password-123"),
            role=UserRole.secretary,
            must_change_password=True,
        )
    )
    db_session.commit()

    assert login(client, "new.user").status_code == 200
    assert client.get("/dashboard").status_code == 403


def test_inactive_user_cannot_login(client, db_session):
    seed_rbac(db_session)
    db_session.add(
        User(
            full_name="کاربر غیرفعال",
            username="inactive.user",
            password_hash=hash_password("test-password-123"),
            role=UserRole.secretary,
            is_deleted=True,
            must_change_password=False,
        )
    )
    db_session.commit()

    response = client.post(
        "/login",
        data={"username": "inactive.user", "password": "test-password-123"},
        follow_redirects=False,
    )
    assert response.status_code == 401
