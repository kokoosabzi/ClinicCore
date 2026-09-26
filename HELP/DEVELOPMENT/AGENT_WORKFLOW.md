# ClinicCore — AI Agent Development Workflow

## 1. نقش این سند

این سند قرارداد کاری Codex و سایر AI Agentها است.

Agent باید قبل از تغییر کد این سند و سایر development specs را بخواند.

## 1.5 Continuity System (Git-based, session-independent)

ClinicCore uses a Git-committed development continuity system so that
any agent — after session expiration, context loss, plan/usage limits,
connection failure, or a handoff to a different AI agent — can resume
work without access to prior conversation history.

The system consists of:

- `HELP/CONTINUE_DEVELOPMENT.txt` — the reusable, step-by-step resume
  instruction. Any agent starting a session on this repository should
  follow it before reading anything else in this section.
- `HELP/DEVELOPMENT/PROGRESS.md` — the single source of truth for
  current phase, current task, task status, completed/in-progress/
  not-started work, last verification, current blockers, and the exact
  next action. **This file must be re-read at the start of every
  session and updated before every session ends.**
- `HELP/DEVELOPMENT/DECISIONS.md` — durable architectural/product
  decisions made during this redesign effort (separate from the
  original `HELP/DECISIONS.txt`). Not for routine implementation notes.
- `HELP/DEVELOPMENT/CHANGELOG_DEV.md` — a concise, chronological log of
  development milestones and commits (separate from `HELP/CHANGELOG.txt`).

Rule: **Rule Zero (section 2) is not satisfied by inspecting the
repository alone.** For any task after the continuity system exists,
inspecting the repository means reading `PROGRESS.md` and
`DECISIONS.md` first, then the code. A task must not be started,
and a task's completion must not be recorded, without updating
`PROGRESS.md` per `HELP/CONTINUE_DEVELOPMENT.txt` step 6.

## 2. Rule Zero

**بدون بررسی repository شروع به بازنویسی نکن.**

ترتیب:

1. inspect repository
2. inspect relevant files
3. inspect tests
4. identify existing behavior
5. write plan
6. implement smallest coherent change
7. test
8. verify
9. document
10. commit

## 3. Source of Truth

ترتیب اولویت:

1. کد و تست‌های فعلی برای behavior موجود
2. این development specs برای target behavior
3. `AGENTS.md` برای قواعد agent
4. README/HELP برای context

اگر contradiction وجود داشت:
- آن را گزارش کن.
- تصمیم را حدس نزن.
- برای تغییر بزرگ ابتدا Decision Record ایجاد کن.

## 4. Scope Control

هر task باید scope مشخص داشته باشد.

ممنوع:
- refactor نامرتبط
- تغییر dependency بدون ضرورت
- rename گسترده بدون نیاز
- حذف قابلیت موجود بدون acceptance replacement
- افزودن framework سنگین بدون نیاز

## 5. قبل از تغییر

Agent باید بررسی کند:

```text
git status
git branch
tree / relevant files
tests
configuration
migrations
```

اگر working tree دارای تغییرات کاربر است:
- آن‌ها را overwrite نکن.
- تغییرات را commit یا revert نکن مگر با دستور صریح.

## 6. Implementation

برای هر feature:

```text
Requirement
  ↓
Design
  ↓
Model/schema
  ↓
Service
  ↓
Repository
  ↓
Router/UI
  ↓
Tests
```

در صورت بی‌نیازی یک لایه، دلیل آن ثبت شود.

## 7. Database Changes

هر تغییر schema:
- migration دارد.
- downgrade strategy مشخص دارد.
- روی database واقعی پروژه تست می‌شود.

Enum/type migrationها باید idempotent و قابل تکرار باشند.

## 8. UI Changes

UI feature باید:
- shared component را بررسی کند.
- theme tokens را استفاده کند.
- RTL را حفظ کند.
- back/breadcrumb را رعایت کند.
- print behavior را در صورت ارتباط بررسی کند.

## 9. Tests

حداقل:

```text
python -m compileall app
pytest
```

برای تغییرات UI/API:
- endpoint smoke test
- auth behavior
- relevant manual browser test

## 10. Manual Verification

برای قابلیت‌های UI، فقط test unit کافی نیست.

Agent باید مسیر اصلی را verify کند، مثلاً:

```text
login
→ dashboard
→ target feature
→ save
→ return
→ verify persisted value
```

## 11. Commit Strategy

Commitهای کوچک و معنایی:

```text
feat(settings): add system settings service
feat(ui): add global page navigation
feat(calendar): add jalali date service
feat(reporting): add dashboard metrics
fix(print): correct receipt layout
test(settings): add settings acceptance tests
```

یک commit نباید شامل چند feature مستقل باشد.

## 12. Documentation

هر behavior جدید:
- requirement
- relevant spec
- migration note
- usage note

را در صورت نیاز به‌روز کند.

## 13. Secrets

Agent هرگز:
- password واقعی
- API token
- database credential
- private key

را commit نکند.

## 14. Dependencies

قبل از افزودن dependency:
1. قابلیت استاندارد/موجود را بررسی کن.
2. dependency موجود را بررسی کن.
3. فقط در صورت نیاز واقعی dependency اضافه کن.
4. pyproject را به‌روز کن.
5. نصب و test را انجام بده.

## 15. Database Transition

در migration به SQLite:
- PostgreSQL فعلی را تا پایان migration strategy حذف نکن.
- SQLite را در محیط test و runtime واقعی اجرا کن.
- compatibility issues را ثبت کن.
- migrationهای Alembic را verify کن.

## 16. Completion Criteria

Task فقط وقتی complete است که:
- implementation done
- tests pass
- manual verification done when needed
- docs updated
- git diff reviewed
- no accidental files staged
- commit created

## 17. Stop Conditions

اگر Agent با این موارد مواجه شد، متوقف و گزارش بدهد:
- destructive migration
- ambiguous product decision
- authentication/security regression
- loss of user data
- unknown external API contract
- conflicting requirements

Agent نباید با حدس، این موارد را حل کند.

## 18. First Task for Codex

پس از نصب این docs، Codex باید ابتدا:

> Repository را inspect کن، این اسناد را بخوان، Gap Analysis بنویس، وضعیت فعلی را با requirements مقایسه کن و یک implementation plan مرحله‌بندی‌شده ارائه بده. هنوز implementation گسترده را شروع نکن.

خروجی باید شامل:
- موجود است
- ناقص است
- وجود ندارد
- risk
- proposed order
باشد.

**Note (added once the Gap Analysis and continuity system exist):**
The Gap Analysis described above has been produced, and the continuity
system in section 1.5 is now in place. For every session *after* that
point, the first task is **not** to redo this Gap Analysis — it is to
follow `HELP/CONTINUE_DEVELOPMENT.txt`, starting from
`HELP/DEVELOPMENT/PROGRESS.md`'s "Exact next action". Only redo or
extend the Gap Analysis if `PROGRESS.md`/`DECISIONS.md` explicitly call
for it (e.g. specs changed materially since the last analysis).
