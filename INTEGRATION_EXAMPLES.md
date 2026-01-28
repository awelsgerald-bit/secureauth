# Code Examples and Integration Guide

## Frontend Integration Examples

### 1. 2FA Setup Flow (JavaScript/React)

```javascript
import React, { useState } from 'react';
import axios from 'axios';

function TwoFactorSetup() {
  const [qrCode, setQrCode] = useState(null);
  const [secret, setSecret] = useState(null);
  const [verificationCode, setVerificationCode] = useState('');
  const [backupCodes, setBackupCodes] = useState([]);
  const [step, setStep] = useState('setup'); // setup, verify, done

  const initiate2FA = async () => {
    try {
      const response = await axios.post('http://localhost:5000/setup-2fa');
      setQrCode(response.data.qrcode);
      setSecret(response.data.secret);
      setStep('verify');
    } catch (error) {
      console.error('Failed to setup 2FA:', error);
    }
  };

  const verify2FA = async () => {
    try {
      const response = await axios.post(
        'http://localhost:5000/confirm-2fa',
        { code: verificationCode }
      );
      setBackupCodes(response.data.backup_codes);
      setStep('done');
    } catch (error) {
      alert('Invalid code. Please try again.');
    }
  };

  return (
    <div className="2fa-setup">
      {step === 'setup' && (
        <div>
          <h2>Setup Two-Factor Authentication</h2>
          <button onClick={initiate2FA}>Start Setup</button>
        </div>
      )}

      {step === 'verify' && (
        <div>
          <h2>Scan QR Code</h2>
          <img src={qrCode} alt="2FA QR Code" />
          <p>Scan this QR code with your authenticator app</p>
          
          <input
            type="text"
            maxLength="6"
            placeholder="Enter 6-digit code"
            value={verificationCode}
            onChange={(e) => setVerificationCode(e.target.value)}
          />
          <button onClick={verify2FA}>Verify Code</button>
        </div>
      )}

      {step === 'done' && (
        <div>
          <h2>✓ 2FA Enabled!</h2>
          <p>Save these backup codes in a safe place:</p>
          <ul>
            {backupCodes.map((code, i) => (
              <li key={i}>{code}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TwoFactorSetup;
```

### 2. Login with 2FA (JavaScript/React)

```javascript
import React, { useState } from 'react';
import axios from 'axios';

function LoginWith2FA() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [requires2FA, setRequires2FA] = useState(false);
  const [userId, setUserId] = useState(null);
  const [code2FA, setCode2FA] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/login',
        { username, password }
      );

      if (response.status === 203) {
        // 2FA required
        setUserId(response.data.user_id);
        setRequires2FA(true);
      } else {
        // Login successful
        localStorage.setItem('user_id', response.data.user_id);
        window.location.href = '/dashboard';
      }
    } catch (error) {
      alert('Login failed: ' + error.response.data.message);
    }
  };

  const handleVerify2FA = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/verify-2fa',
        {
          user_id: userId,
          code: code2FA
        }
      );
      localStorage.setItem('user_id', response.data.user_id);
      window.location.href = '/dashboard';
    } catch (error) {
      alert('Invalid 2FA code');
    }
  };

  if (requires2FA) {
    return (
      <form onSubmit={handleVerify2FA}>
        <h2>Enter 2FA Code</h2>
        <input
          type="text"
          maxLength="6"
          placeholder="6-digit code"
          value={code2FA}
          onChange={(e) => setCode2FA(e.target.value)}
          required
        />
        <button type="submit">Verify</button>
      </form>
    );
  }

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginWith2FA;
```

### 3. Google OAuth Login (JavaScript/React)

```javascript
import React from 'react';
import axios from 'axios';

function GoogleLoginButton() {
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // Decode JWT (install jwt-decode: npm install jwt-decode)
      const jwt_decode = require('jwt-decode');
      const decodedToken = jwt_decode(credentialResponse.credential);

      // Send to backend
      const response = await axios.post(
        'http://localhost:5000/google-login',
        {
          google_id: decodedToken.sub,
          email: decodedToken.email,
          name: decodedToken.name
        }
      );

      // Login successful
      localStorage.setItem('user_id', response.data.user_id);
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Google login failed:', error);
    }
  };

  return (
    <div
      id="g_id_onload"
      data-client_id="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
      data-callback="handleGoogleSuccess"
    >
    </div>
  );
}

export default GoogleLoginButton;
```

### 4. GitHub OAuth Login (JavaScript)

```javascript
// GitHub OAuth flow (backend implementation)
async function handleGitHubCallback(code) {
  try {
    // Exchange code for access token (do this on backend for security)
    const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json'
      },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code: code
      })
    });

    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.access_token;

    // Get user info
    const userResponse = await fetch('https://api.github.com/user', {
      headers: { Authorization: `token ${accessToken}` }
    });
    const userData = await userResponse.json();

    // Send to backend
    const loginResponse = await fetch('http://localhost:5000/github-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        github_id: userData.id,
        login: userData.login,
        email: userData.email
      })
    });

    const result = await loginResponse.json();
    localStorage.setItem('user_id', result.user_id);
    window.location.href = '/dashboard';
  } catch (error) {
    console.error('GitHub login failed:', error);
  }
}
```

## Backend Integration Examples

### Using the API with Python Requests

```python
import requests
import json

BASE_URL = 'http://localhost:5000'

class AuthClient:
    def __init__(self):
        self.session = requests.Session()
    
    def register(self, username, email, password):
        """Register a new user"""
        response = self.session.post(
            f'{BASE_URL}/register',
            json={'username': username, 'email': email, 'password': password}
        )
        return response.json()
    
    def login(self, username, password):
        """Login and get user_id"""
        response = self.session.post(
            f'{BASE_URL}/login',
            json={'username': username, 'password': password}
        )
        return response.json()
    
    def setup_2fa(self):
        """Setup 2FA"""
        response = self.session.post(f'{BASE_URL}/setup-2fa')
        return response.json()
    
    def verify_2fa(self, user_id, code):
        """Verify 2FA code"""
        response = self.session.post(
            f'{BASE_URL}/verify-2fa',
            json={'user_id': user_id, 'code': code}
        )
        return response.json()
    
    def google_login(self, google_id, email, name):
        """Login with Google"""
        response = self.session.post(
            f'{BASE_URL}/google-login',
            json={'google_id': google_id, 'email': email, 'name': name}
        )
        return response.json()
    
    def get_profile(self):
        """Get current user profile"""
        response = self.session.get(f'{BASE_URL}/profile')
        return response.json()

# Usage
client = AuthClient()

# Register
result = client.register('john', 'john@example.com', 'SecurePass123!')
print(result)

# Login
login_result = client.login('john', 'SecurePass123!')
if login_result.get('2fa_required'):
    print('2FA Required!')
    user_id = login_result['user_id']
    # Get 2FA code from user
    code = input('Enter 2FA code: ')
    result = client.verify_2fa(user_id, code)
    print(result)
```

## Environment Configuration

### .env File Example

```
# App Configuration
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=development
FLASK_DEBUG=True

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///auth_system.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@authsystem.com

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Server Configuration
SERVER_NAME=localhost:5000
PREFERRED_URL_SCHEME=http
```

### Load Environment Variables

```python
# In app.py or config.py
from dotenv import load_dotenv
import os

load_dotenv()

# Now use os.environ.get('VARIABLE_NAME')
```

## Testing Helper Functions

```python
# Test helper utilities
def create_test_user():
    """Create a test user"""
    from models import User, db
    user = User(
        username='testuser',
        email='test@example.com'
    )
    user.set_password('TestPassword123!')
    db.session.add(user)
    db.session.commit()
    return user

def verify_test_user(user):
    """Verify email for test user"""
    user.email_verified = True
    user.is_active = True
    user.verification_token = None
    db.session.commit()

def test_api_flow():
    """Test complete authentication flow"""
    user = create_test_user()
    verify_test_user(user)
    
    # Test login
    response = requests.post(
        f'{BASE_URL}/login',
        json={'username': 'testuser', 'password': 'TestPassword123!'}
    )
    assert response.status_code == 200
    print('✓ Login successful')
```

## Deployment Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure email service (SendGrid, AWS SES)
- [ ] Setup OAuth credentials (Google, GitHub)
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Configure CORS if needed
- [ ] Add rate limiting
- [ ] Enable database backups
- [ ] Setup error tracking (Sentry)
- [ ] Configure CDN for assets
- [ ] Set up CI/CD pipeline

## Common Issues & Solutions

### "401 Please verify your email first"
- User hasn't verified email yet
- Solution: Check verification email, click link

### "Invalid 2FA code"
- Code expired (valid for 30 seconds)
- Wrong code
- Solution: Try next code, check time sync

### "Google login failed"
- Invalid google_id or email
- CORS error
- Solution: Check OAuth config, enable CORS

### "Email not sending"
- Wrong MAIL_USERNAME/MAIL_PASSWORD
- Email service blocked
- Solution: Use app password for Gmail, whitelist service

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PyOTP Documentation](https://pyotp.readthedocs.io/)
- [Google OAuth](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth](https://docs.github.com/en/developers/apps/building-oauth-apps)
