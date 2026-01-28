# Flask Authentication System

A complete Flask authentication system with email verification, password reset, and user management.

## Features

- ✅ User Registration with Email Verification
- ✅ Secure Login/Logout with Password Hashing
- ✅ Password Reset with Email Link
- ✅ Change Password for Logged-in Users
- ✅ Email Verification Tokens
- ✅ Resend Verification Email
- ✅ User Profile Management
- ✅ Remember Me Functionality
- ✅ SQLAlchemy Database Models
- ✅ Flask-Migrate for Database Migrations
- ✅ Comprehensive Unit Tests
- ✅ HTML Templates with Modern UI

## Project Structure

```
FlaskAuthSystem/
├── app.py                 # Flask application factory
├── config.py             # Configuration settings
├── models.py             # Database models
├── routes.py             # Authentication routes
├── test_auth.py          # Unit tests
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── templates/
    ├── base.html
    ├── register.html
    ├── login.html
    ├── profile.html
    ├── forgot_password.html
    └── reset_password.html
```

## Installation

1. **Clone or create the project:**
   ```bash
   cd FlaskAuthSystem
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional):**
   ```bash
   # Create a .env file
   SECRET_KEY=your-secret-key
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

## Running the Application

```bash
python app.py
```

The application will run on `http://localhost:5000`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| POST | `/register` | Register a new user | No |
| GET | `/verify-email/<token>` | Verify email | No |
| POST | `/login` | Login user | No |
| POST | `/logout` | Logout user | Yes |
| GET | `/profile` | Get user profile | Yes |
| POST | `/forgot-password` | Request password reset | No |
| POST | `/reset-password/<token>` | Reset password | No |
| POST | `/change-password` | Change password | Yes |
| POST | `/resend-verification` | Resend verification email | No |

## Testing

Run the test suite:

```bash
pytest test_auth.py -v
```

For coverage report:

```bash
pytest test_auth.py --cov=. --cov-report=html
```

## Database Migrations

Create a new migration:

```bash
flask db migrate -m "Add new column"
```

Apply migrations:

```bash
flask db upgrade
```

Downgrade:

```bash
flask db downgrade
```

## Security Features

- ✅ Password Hashing with Werkzeug
- ✅ CSRF Protection Ready
- ✅ Token-based Email Verification
- ✅ Secure Password Reset Tokens
- ✅ Email Verification Required
- ✅ Token Expiry (24 hours for email, 1 hour for reset)

## Configuration

Edit `config.py` to customize:

- Database URI
- Email settings
- Session timeout
- Secret key
- Mail server settings

## Email Setup (Gmail Example)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Set environment variables:
   ```bash
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

## Future Enhancements

- [ ] Social login (Google, GitHub)
- [ ] Two-factor authentication
- [ ] User roles and permissions
- [ ] Admin dashboard
- [ ] API key authentication
- [ ] Rate limiting
- [ ] Account lockout after failed attempts
- [ ] Email templates

## License

MIT License

## Support

For issues or questions, please check the Flask documentation or create an issue.
