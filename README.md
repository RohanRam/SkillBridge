# SkillBridge Attendance Management API

> **Note:** The API is designed for the SkillBridge Attendance system. 

## Live API Deployment
**Base URL:** `https://skillbridge-api-tztw.onrender.com`

*(Check out the interactive API documentation at [https://skillbridge-api-tztw.onrender.com/docs](https://skillbridge-api-tztw.onrender.com/docs))*

## Local Setup

Assume Python 3.9+ and pip are installed.

1. Clone the repository and navigate into it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the environment variables:
   ```bash
   # Copy the example env
   cp .env.example .env
   # Ensure .env contains DATABASE_URL=sqlite:///./skillbridge.db
   ```
4. Seed the database with test data:
   ```bash
   python src/seed.py
   ```
5. Run the application locally:
   ```bash
   uvicorn src.main:app --reload
   ```

## Test Accounts

The seed script creates the following accounts (all use the password `password123`):

| Role | Email |
|------|-------|
| Student | `student1@test.com` |
| Trainer | `trainer1@test.com` |
| Institution | `inst1@test.com` |
| Programme Manager | `pm@test.com` |
| Monitoring Officer | `mo@test.com` |

## Token & Authentication Design

### JWT Payload Structure
- **Standard Token:** `{ "user_id": 1, "role": "student", "exp": 1700000000, "iat": 1699913600 }`
- **Monitoring Token:** `{ "user_id": 2, "role": "monitoring_officer", "scope": "monitoring", "exp": 1700003600, ... }`

### Token Rotation & Revocation
Currently, JWTs are stateless. In a real deployment, I would implement a Redis-based blocklist (or allowlist) to revoke tokens instantly if an account is compromised. Alternatively, keeping a `token_version` on the user record in the DB (and including it in the JWT) allows mass revocation of a user's tokens by simply incrementing their `token_version` in the database.

### Security Issue & Future Fix
**Issue:** Passwords have a max length limitation when using `bcrypt` (72 bytes). 
**Fix:** With more time, I would first hash the password with `SHA-256` (resulting in a consistent 64-character hex string) before passing it to `bcrypt`. This prevents the 72-byte truncation limit while maintaining bcrypt's work factor security.

## Schema Decisions

1. **`batch_trainers` and `batch_students` (Many-to-Many):** Since multiple trainers can manage the same batch and a student can potentially join multiple batches (or at least it's a many-to-many logically), association tables were used.
2. **`batch_invites`:** The invite token is completely detached from the user model. It belongs to the batch and tracks `created_by` and an `expires_at` timestamp. This allows safe, shareable links.
3. **Dual-Token System (Monitoring Officer):** To fulfill the extra security layer, the Monitoring Officer logs in normally, then hits a specialized route (`/auth/monitoring-token`) with their standard JWT and a hardcoded API Key. They receive a 1-hour token with an explicit `"scope": "monitoring"` claim, isolating read-only data access from general access.

## Curl Commands

**Login (Trainer):**
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=trainer1@test.com&password=password123"
```

**Get Monitoring Token:**
```bash
# Assuming $STANDARD_TOKEN is set
curl -X POST http://127.0.0.1:8000/auth/monitoring-token \
     -H "Authorization: Bearer $STANDARD_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key": "testmonitoringkey"}'
```

**View All Attendance (Monitoring Officer):**
```bash
# Assuming $MONITORING_TOKEN is set
curl -X GET http://127.0.0.1:8000/monitoring/attendance \
     -H "Authorization: Bearer $MONITORING_TOKEN"
```

## What's Working
- Full Auth & JWT generation (both standard and scoped monitoring).
- Role-Based Access Control on every protected endpoint.
- Database modeling with SQLAlchemy.
- Data validation and error handling via Pydantic/FastAPI.
- Pytest suite successfully testing database models and core API flows.

## What's Skipped / Limitations
- Deployment scripts (e.g. Dockerfile). The user is required to set up their own platform variables (Railway/Render) and attach their Neon Postgres DB URL.
- Front-end integration (pure API as requested).

## If I had more time...
I would implement comprehensive logging using `structlog` or Python's native logging to track exactly when and who hits the endpoints. I would also add Alembic for database migrations instead of relying on `Base.metadata.create_all()`.
