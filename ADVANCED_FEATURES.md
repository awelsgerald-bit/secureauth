# Advanced Features Guide

## 2FA (Two-Factor Authentication)

### Setup 2FA

1. **Initiate 2FA Setup** (User must be logged in)
   ```bash
   POST /setup-2fa
   
   Response:
   {
     "message": "2FA setup initiated",
     "secret": "JBSWY3DPEBLW64TMMQ======",
     "qrcode": "data:image/png;base64,..."
   }
   ```

2. **Confirm 2FA with Code**
   ```bash
   POST /confirm-2fa
   Content-Type: application/json
   
   {
     "code": "123456"
   }
   
   Response:
   {
     "message": "2FA enabled successfully",
     "backup_codes": [
       "code1", "code2", "code3", ...
     ]
   }
   ```
   
   **Save backup codes in a safe place!** They can be used if you lose access to your authenticator app.

### Login with 2FA

1. **Initial Login**
   ```bash
   POST /login
   Content-Type: application/json
   
   {
     "username": "testuser",
     "password": "SecurePassword123!"
   }
   
   Response: (2FA Enabled)
   {
     "message": "2FA required",
     "user_id": 1,
     "2fa_required": true
   }
   ```

2. **Verify 2FA Code**
   ```bash
   POST /verify-2fa
   Content-Type: application/json
   
   {
     "user_id": 1,
     "code": "123456"  // From authenticator app
   }
   
   Response:
   {
     "message": "2FA verified. Login successful.",
     "user_id": 1
   }
   ```

   **Or use a backup code:**
   ```bash
   {
     "user_id": 1,
     "code": "backup-code-1"
   }
   ```

### Disable 2FA

```bash
POST /disable-2fa
(User must be logged in)

Response:
{
  "message": "2FA disabled successfully"
}
```

## Social Login (OAuth)

### Google Login

1. **Frontend**: Get Google ID token from Google OAuth
2. **Backend**: Send to your server
   ```bash
   POST /google-login
   Content-Type: application/json
   
   {
     "google_id": "110169268886007....",
     "email": "user@gmail.com",
     "name": "John Doe"
   }
   
   Response:
   {
     "message": "Google login successful",
     "user_id": 1,
     "username": "john-doe"
   }
   ```

### GitHub Login

1. **Frontend**: Get GitHub code, exchange for access token
2. **Backend**: Get user info from GitHub API, send to server
   ```bash
   POST /github-login
   Content-Type: application/json
   
   {
     "github_id": 12345678,
     "login": "johndoe",
     "email": "user@github.com"
   }
   
   Response:
   {
     "message": "GitHub login successful",
     "user_id": 2,
     "username": "johndoe"
   }
   ```

### Link OAuth to Existing Account

Link a social provider to an existing account:

```bash
POST /link-oauth
Content-Type: application/json
(User must be logged in)

{
  "provider": "google",  // or "github"
  "provider_id": "110169268886007...."
}

Response:
{
  "message": "google account linked successfully"
}
```

## Testing with cURL

### Test 2FA Setup
```bash
# Login first
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"SecurePassword123!"}'

# Setup 2FA
curl -X POST http://localhost:5000/setup-2fa \
  -H "Content-Type: application/json"

# Confirm with code (replace with real code from authenticator)
curl -X POST http://localhost:5000/confirm-2fa \
  -H "Content-Type: application/json" \
  -d '{"code":"123456"}'
```

### Test Google Login
```bash
curl -X POST http://localhost:5000/google-login \
  -H "Content-Type: application/json" \
  -d '{
    "google_id": "test-google-id",
    "email": "user@gmail.com",
    "name": "Test User"
  }'
```

## Recommended Authenticator Apps for 2FA

- Google Authenticator
- Microsoft Authenticator
- Authy
- 1Password
- LastPass
- FreeOTP

## Frontend Implementation Tips

### For 2FA QR Code Display
```javascript
// After /setup-2fa response
const qrcode = response.qrcode;
document.getElementById('qr-image').src = qrcode;
```

### For Google OAuth
```javascript
// Use Google Sign-In library
google.accounts.id.initialize({
  client_id: 'YOUR_CLIENT_ID.apps.googleusercontent.com'
});

google.accounts.id.renderButton(document.getElementById('buttonDiv'), {
  theme: 'outline',
  size: 'large'
});

function handleGoogleLogin(response) {
  fetch('/google-login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      google_id: response.credential,
      email: response.email,
      name: response.name
    })
  });
}
```

### For GitHub OAuth
```javascript
// After user authorizes, GitHub redirects with code
const params = new URLSearchParams(window.location.search);
const code = params.get('code');

// Exchange code for token on your backend
fetch('/github-callback', {
  method: 'POST',
  body: JSON.stringify({ code })
});

// Then login with GitHub data
fetch('/github-login', {
  method: 'POST',
  body: JSON.stringify({
    github_id: userData.id,
    login: userData.login,
    email: userData.email
  })
});
```

## Security Notes

1. **Never** share 2FA backup codes
2. **Always** use HTTPS in production
3. **Store** backup codes securely (password manager)
4. **Regenerate** OAuth tokens regularly
5. **Validate** all OAuth responses server-side
6. **Use** environment variables for OAuth secrets

## Troubleshooting

### 2FA Code Not Working
- Ensure server time is synchronized with authenticator app
- Code expires after 30 seconds
- Try the next code if at boundary

### Google Login Not Working
- Verify google_id is the correct format
- Check CORS settings if frontend is different domain
- Validate OAuth app configuration

### GitHub Login Issues
- Ensure GitHub callback URL matches your app settings
- Verify scopes requested in OAuth flow
- Check GitHub API rate limits
