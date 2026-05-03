# 🚀 Python Developer Intern Assignment — Complete Implementation Guide

## 📌 Overview
This document is a **complete, production-ready blueprint** to build the SkillBridge Attendance Management API.

It includes:
- Architecture
- Database schema
- API design
- Authentication (JWT + Monitoring Token)
- RBAC
- Testing
- Deployment
- README template

---

# 🧠 System Architecture

## Layers
1. **Frontend (optional)**
2. **Backend (FastAPI)**
3. **Database (PostgreSQL - Neon)**
4. **Auth Layer (JWT)**
5. **Deployment (Render/Railway)**

---

# 🗄️ Database Schema

## Users
- id
- name
- email
- hashed_password
- role
- institution_id
- created_at

## Batches
- id
- name
- institution_id
- created_at

## Batch Trainers
- batch_id
- trainer_id

## Batch Students
- batch_id
- student_id

## Batch Invites
- id
- batch_id
- token
- created_by
- expires_at
- used

## Sessions
- id
- batch_id
- trainer_id
- title
- date
- start_time
- end_time
- created_at

## Attendance
- id
- session_id
- student_id
- status
- marked_at

---

# 🔐 Authentication System

## JWT Payload
```json
{
  "user_id": 1,
  "role": "student",
  "iat": "...",
  "exp": "..."
}
```

## Token Rules
- Expiry: 24 hours
- Algorithm: HS256

---

# 👁 Monitoring Officer Special Flow

1. Login → get JWT
2. Call `/auth/monitoring-token`
3. Provide API Key
4. Receive short-lived token (1 hour)
5. Use token for monitoring endpoints

---

# 🔌 API Endpoints

## Auth
- POST /auth/signup
- POST /auth/login
- POST /auth/monitoring-token

## Batches
- POST /batches
- POST /batches/{id}/invite
- POST /batches/join

## Sessions
- POST /sessions

## Attendance
- POST /attendance/mark

## Reports
- GET /sessions/{id}/attendance
- GET /batches/{id}/summary
- GET /institutions/{id}/summary
- GET /programme/summary

## Monitoring
- GET /monitoring/attendance

---

# 🔒 Role-Based Access Control

| Role | Permissions |
|------|-----------|
| Student | Mark attendance |
| Trainer | Create sessions, manage batches |
| Institution | View batch summary |
| Programme Manager | View all summaries |
| Monitoring Officer | Read-only access |

---

# ⚠️ Validation Rules
- Missing fields → 422
- Invalid IDs → 404
- Unauthorized → 403
- No token → 401
- Wrong method → 405

---

# 🧪 Testing (pytest)

## Required Tests
1. Signup + Login
2. Trainer creates session
3. Student marks attendance
4. POST on monitoring → 405
5. No token → 401

---

# 🚀 Deployment Guide

## Backend
- Use Render or Railway

## Database
- Neon PostgreSQL

## Steps
1. Push to GitHub
2. Connect to Render
3. Add environment variables
4. Deploy

---

# 📄 README Template

## Include:
- API Base URL
- Setup Instructions
- Test Accounts
- Curl Commands
- JWT explanation
- What works / not
- Future improvements

---

# ⚡ Folder Structure

```
/src
  /models
  /routes
  /schemas
  /services
/tests
README.md
requirements.txt
.env.example
```

---

# 💡 Improvements
- Token revocation
- Rate limiting
- Logging
- Docker support

---

# ✅ Final Advice
- Focus on working system
- Don't over-engineer
- Document everything honestly

---

# 🎯 Outcome
If you follow this guide, you will have:
✔ Fully functional backend  
✔ Secure JWT system  
✔ Proper RBAC  
✔ Deployment-ready API  
✔ Strong chance of selection