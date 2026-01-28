# Quick Reference Guide

## All API Endpoints

### 🔐 Authentication (5 endpoints)

```
POST   /register                    - Register new user
GET    /verify-email/<token>        - Verify email with token
POST   /login                       - Login user
POST   /logout                      - Logout user (protected)
GET    /profile                     - Get user profile (protected)
```

### 🔑 Two-Factor Authentication (4 endpoints)

```
POST   /setup-2fa                   - Initiate 2FA setup (protected)
POST   /confirm-2fa                 - Confirm 2FA with code (protected)
POST   /verify-2fa                  - Verify 2FA during login
POST   /disable-2fa                 - Disable 2FA (protected)
```

### 🌐 Social Login / OAuth (3 endpoints)

```
POST   /google-login                - Login with Google
POST   /github-login                - Login with GitHub
POST   /link-oauth                  - Link OAuth to account (protected)
```

### 🔑 Password Management (3 endpoints)

```
POST   /forgot-password             - Request password reset
POST   /reset-password/<token>      - Reset password with token
POST   /change-password             - Change password (protected)
```

### ✉️ Email Management (2 endpoints)

```
POST   /resend-verification         - Resend verification email
```

### 🏠 Home (1 endpoint)

```
GET    /                            - Home endpoint
```

**Total: 17 Endpoints**

---

## Quick API Calls

### Register User
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "SecurePass123!"
  }'
```

### Setup 2FA
```bash
curl -X POST http://localhost:5000/setup-2fa
```

### Verify 2FA Code
```bash
curl -X POST http://localhost:5000/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "code": "123456"
  }'
```

### Google OAuth
```bash
curl -X POST http://localhost:5000/google-login \
  -H "Content-Type: application/json" \
  -d '{
    "google_id": "110169268886007...",
    "email": "user@gmail.com",
    "name": "John Doe"
  }'
```

### GitHub OAuth
```bash
curl -X POST http://localhost:5000/github-login \
  -H "Content-Type: application/json" \
  -d '{
    "github_id": 12345678,
    "login": "johndoe",
    "email": "john@github.com"
  }'
```

### Get Profile
```bash
curl -X GET http://localhost:5000/profile \
  -H "Cookie: session=your_session_id"
```

### Change Password
```bash
curl -X POST http://localhost:5000/change-password \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "OldPassword123!",
    "new_password": "NewPassword456!"
  }'
```

### Forgot Password
```bash
curl -X POST http://localhost:5000/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```

---

## Response Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful request |
| 201 | Created | User registered successfully |
| 203 | No Content | 2FA required |
| 301 | Moved Permanently | Redirect (login required) |
| 302 | Found | Redirect |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication failed |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | Wrong HTTP method |

---

## Request/Response Examples

### Successful Login
**Request:**
```json
{
  "username": "john",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "username": "john"
}
```

### Login with 2FA Enabled
**Response (203):**
```json
{
  "message": "2FA required",
  "user_id": 1,
  "2fa_required": true
}
```

### Register User
**Response (201):**
```json
{
  "message": "User registered. Check your email to verify."
}
```

### Get Profile
**Response (200):**
```json
{
  "user_id": 1,
  "username": "john",
  "email": "john@example.com",
  "email_verified": true,
  "2fa_enabled": true,
  "oauth_provider": null,
  "created_at": "2026-01-28T10:30:00"
}
```

---

## File Structure

```
FlaskAuthSystem/
├── app.py                          # Main Flask app
├── config.py                       # Configuration
├── models.py                       # Database models
├── routes.py                       # API routes
├── test_auth.py                    # Unit tests (10 tests)
├── test_api_requests.py            # API integration tests
├── postman_collection.json         # Postman collection
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git configuration
├── README.md                       # Basic documentation
├── ADVANCED_FEATURES.md            # 2FA & OAuth guide
├── INTEGRATION_EXAMPLES.md         # Code examples
├── IMPLEMENTATION_SUMMARY.md       # This summary
├── QUICK_REFERENCE.md              # This file
├── templates/                      # HTML templates
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   ├── forgot_password.html
│   └── reset_password.html
└── auth_system.db                  # SQLite database (created on first run)
```

---

## Environment Variables (.env)

```
# Essential
SECRET_KEY=your-secret-key
FLASK_ENV=development

# Email (for password reset, verification)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# OAuth (optional, only if using social login)
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
```

---

## Running the System

### Start Server
```bash
python app.py
# Server runs on http://127.0.0.1:5000
```

### Run Tests
```bash
# Unit tests
python -m pytest test_auth.py -v

# API tests
python test_api_requests.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Database Schema (Auto-created)

### User Table
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key |
| username | String | Unique |
| email | String | Unique |
| password_hash | String | Hashed password |
| is_active | Boolean | Account active |
| email_verified | Boolean | Email verified |
| verification_token | String | Email verification |
| reset_token | String | Password reset |
| two_fa_enabled | Boolean | 2FA enabled |
| two_fa_secret | String | TOTP secret |
| two_fa_backup_codes | Text | JSON backup codes |
| google_id | String | Google OAuth ID |
| github_id | String | GitHub OAuth ID |
| oauth_provider | String | OAuth provider |
| created_at | DateTime | Account created |
| updated_at | DateTime | Last updated |

---

## Security Checklist

- ✓ Passwords hashed with Werkzeug
- ✓ Email verification required
- ✓ Password reset tokens (1-hour expiry)
- ✓ 2FA TOTP support
- ✓ Backup codes for 2FA
- ✓ OAuth provider support
- ✓ Session management
- ✓ CSRF protection ready

---

## Common Workflows

### Complete Registration + Login Flow
```
1. POST /register          → User created, not verified
2. Email sent with link    → User clicks link
3. GET /verify-email/:token → Email verified
4. POST /login             → User logged in
```

### 2FA Setup Flow
```
1. POST /setup-2fa         → Get QR code + secret
2. User scans QR code      → Add to authenticator app
3. POST /confirm-2fa       → Verify code + enable 2FA
4. Save backup codes       → Store securely
```

### Password Reset Flow
```
1. POST /forgot-password   → Email sent with reset link
2. User clicks link        → Redirected to reset page
3. POST /reset-password    → Enter new password
4. Password updated        → Can login with new password
```

### Google OAuth Login
```
1. Frontend: Google Sign-In → Get ID token
2. POST /google-login      → Send token to backend
3. Backend: Create/login user → Return user_id
4. Frontend: Login complete → Redirect to dashboard
```

---

## Testing with Postman

1. **Import Collection**
   - File → Import → `postman_collection.json`

2. **Set Variables**
   - `base_url`: `http://127.0.0.1:5000`
   - `verification_token`: From email
   - `reset_token`: From email

3. **Test Endpoints**
   - Click endpoint → Send
   - Check Status and Response

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Start app: `python app.py` |
| "Email not sending" | Set MAIL_USERNAME/MAIL_PASSWORD |
| "2FA code invalid" | Code expires in 30 seconds, try next one |
| "Email already verified" | Already verified, try login |
| "Token expired" | Tokens expire (24h for email, 1h for password) |
| "CORS error" | Add CORS headers (optional) |

---

## Performance Tips

- Use PostgreSQL for production
- Add caching for profiles
- Enable connection pooling
- Use CDN for static files
- Add rate limiting
- Monitor with Sentry

---

## Next Steps

1. ✅ Test all endpoints
2. ✅ Setup email configuration
3. ✅ Create frontend app
4. ✅ Deploy to production
5. ✅ Monitor and maintain

---

## Support & Documentation

- **Full Guide**: See `README.md`
- **Advanced Features**: See `ADVANCED_FEATURES.md`
- **Code Examples**: See `INTEGRATION_EXAMPLES.md`
- **Implementation**: See `IMPLEMENTATION_SUMMARY.md`
- **Tests**: Run `test_auth.py` or `test_api_requests.py`

---

**Everything you need is here! 🚀**
