from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import pyotp
import qrcode
from io import BytesIO
import base64

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), unique=True)
    verification_token_expiry = db.Column(db.DateTime)
    reset_token = db.Column(db.String(255), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    
    # Two-Factor Authentication
    two_fa_enabled = db.Column(db.Boolean, default=False)
    two_fa_secret = db.Column(db.String(255))
    two_fa_backup_codes = db.Column(db.Text)  # JSON string
    
    # Social Login
    google_id = db.Column(db.String(255), unique=True)
    github_id = db.Column(db.String(255), unique=True)
    oauth_provider = db.Column(db.String(50))  # 'google', 'github', etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def generate_verification_token(self):
        """Generate email verification token"""
        self.verification_token = secrets.token_urlsafe(32)
        self.verification_token_expiry = datetime.utcnow() + timedelta(hours=24)
        return self.verification_token
    
    def verify_email_token(self, token):
        """Verify email verification token"""
        if self.verification_token != token:
            return False
        if datetime.utcnow() > self.verification_token_expiry:
            return False
        self.email_verified = True
        self.is_active = True
        self.verification_token = None
        self.verification_token_expiry = None
        return True
    
    def generate_reset_token(self):
        """Generate password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify password reset token"""
        if self.reset_token != token:
            return False
        if datetime.utcnow() > self.reset_token_expiry:
            return False
        return True
    
    def reset_password(self, password, token):
        """Reset password with token"""
        if not self.verify_reset_token(token):
            return False
        self.set_password(password)
        self.reset_token = None
        self.reset_token_expiry = None
        return True
    
    # Two-Factor Authentication Methods
    def setup_2fa(self):
        """Generate 2FA secret and QR code"""
        self.two_fa_secret = pyotp.random_base32()
        self.two_fa_enabled = False  # Not enabled until verified
        return self.two_fa_secret
    
    def get_2fa_qrcode(self):
        """Generate QR code for 2FA"""
        if not self.two_fa_secret:
            self.setup_2fa()
        
        totp = pyotp.TOTP(self.two_fa_secret)
        uri = totp.provisioning_uri(name=self.email, issuer_name='Flask Auth System')
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def verify_2fa_code(self, code):
        """Verify 2FA code"""
        if not self.two_fa_secret:
            return False
        
        totp = pyotp.TOTP(self.two_fa_secret)
        return totp.verify(code)
    
    def enable_2fa(self):
        """Enable 2FA after verification"""
        self.two_fa_enabled = True
        # Generate backup codes
        import json
        backup_codes = [secrets.token_urlsafe(8) for _ in range(10)]
        self.two_fa_backup_codes = json.dumps(backup_codes)
    
    def get_2fa_backup_codes(self):
        """Get 2FA backup codes"""
        if not self.two_fa_backup_codes:
            return []
        import json
        return json.loads(self.two_fa_backup_codes)
    
    def disable_2fa(self):
        """Disable 2FA"""
        self.two_fa_enabled = False
        self.two_fa_secret = None
        self.two_fa_backup_codes = None
    
    def __repr__(self):
        return f'<User {self.username}>'
