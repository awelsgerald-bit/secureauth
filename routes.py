from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from models import db, User
from app import mail
import json

auth_bp = Blueprint('auth', __name__)

def send_email(subject, recipients, body):
    """Send email helper"""
    try:
        msg = Message(subject, recipients=recipients, body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Create new user
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        token = user.generate_verification_token()
        
        db.session.add(user)
        db.session.commit()
        
        # Send verification email
        verification_link = f"http://localhost:5000/verify-email/{token}"
        send_email(
            'Email Verification',
            [user.email],
            f'Click here to verify your email: {verification_link}'
        )
        
        return jsonify({'message': 'User registered. Check your email to verify.'}), 201
    
    return jsonify({'message': 'Use POST to register'}), 405

@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    """Verify email with token"""
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    if user.verify_email_token(token):
        db.session.commit()
        return jsonify({'message': 'Email verified successfully! You can now log in.'}), 200
    
    return jsonify({'message': 'Token expired or invalid'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.is_active:
        return jsonify({'message': 'Please verify your email first'}), 401
    
    if user and user.check_password(data['password']):
        # Check if 2FA is enabled
        if user.two_fa_enabled:
            return jsonify({
                'message': '2FA required',
                'user_id': user.id,
                '2fa_required': True
            }), 203  # 203 No Content - Need MFA
        
        login_user(user, remember=data.get('remember_me', False))
        return jsonify({'message': 'Login successful', 'user_id': user.id, 'username': user.username}), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    """Verify 2FA code"""
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('code'):
        return jsonify({'message': 'User ID and code are required'}), 400
    
    user = User.query.get(int(data['user_id']))
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if user.verify_2fa_code(data['code']):
        login_user(user, remember=data.get('remember_me', False))
        return jsonify({'message': '2FA verified. Login successful.', 'user_id': user.id}), 200
    
    # Check backup codes
    if data.get('code') in user.get_2fa_backup_codes():
        codes = user.get_2fa_backup_codes()
        codes.remove(data['code'])
        user.two_fa_backup_codes = json.dumps(codes)
        db.session.commit()
        login_user(user, remember=data.get('remember_me', False))
        return jsonify({'message': 'Backup code used. Login successful.'}), 200
    
    return jsonify({'message': 'Invalid 2FA code'}), 401

@auth_bp.route('/setup-2fa', methods=['POST'])
@login_required
def setup_2fa():
    """Setup 2FA for logged-in user"""
    secret = current_user.setup_2fa()
    qrcode = current_user.get_2fa_qrcode()
    db.session.commit()
    
    return jsonify({
        'message': '2FA setup initiated',
        'secret': secret,
        'qrcode': qrcode
    }), 200

@auth_bp.route('/confirm-2fa', methods=['POST'])
@login_required
def confirm_2fa():
    """Confirm 2FA with verification code"""
    data = request.get_json()
    
    if not data or not data.get('code'):
        return jsonify({'message': 'Verification code is required'}), 400
    
    if current_user.verify_2fa_code(data['code']):
        current_user.enable_2fa()
        backup_codes = current_user.get_2fa_backup_codes()
        db.session.commit()
        
        return jsonify({
            'message': '2FA enabled successfully',
            'backup_codes': backup_codes
        }), 200
    
    return jsonify({'message': 'Invalid verification code'}), 400

@auth_bp.route('/disable-2fa', methods=['POST'])
@login_required
def disable_2fa():
    """Disable 2FA"""
    current_user.disable_2fa()
    db.session.commit()
    
    return jsonify({'message': '2FA disabled successfully'}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Get current user profile"""
    return jsonify({
        'user_id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'email_verified': current_user.email_verified,
        '2fa_enabled': current_user.two_fa_enabled,
        'oauth_provider': current_user.oauth_provider,
        'created_at': current_user.created_at.isoformat()
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user:
        token = user.generate_reset_token()
        db.session.commit()
        
        reset_link = f"http://localhost:5000/reset-password/{token}"
        send_email(
            'Password Reset Request',
            [user.email],
            f'Click here to reset your password: {reset_link}'
        )
    
    return jsonify({'message': 'If email exists, password reset link sent'}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    """Reset password with token"""
    user = User.query.filter_by(reset_token=token).first()
    
    if not user:
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    data = request.get_json()
    
    if not data or not data.get('password'):
        return jsonify({'message': 'Password is required'}), 400
    
    if user.reset_password(data['password'], token):
        db.session.commit()
        return jsonify({'message': 'Password reset successful'}), 200
    
    return jsonify({'message': 'Invalid or expired token'}), 400

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change password for logged-in user"""
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'message': 'Old password and new password are required'}), 400
    
    if not current_user.check_password(data['old_password']):
        return jsonify({'message': 'Old password is incorrect'}), 401
    
    current_user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'message': 'Email not found'}), 404
    
    if user.email_verified:
        return jsonify({'message': 'Email already verified'}), 400
    
    token = user.generate_verification_token()
    db.session.commit()
    
    verification_link = f"http://localhost:5000/verify-email/{token}"
    send_email(
        'Email Verification',
        [user.email],
        f'Click here to verify your email: {verification_link}'
    )
    
    return jsonify({'message': 'Verification email sent'}), 200

# Social Login Routes
@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    """Google OAuth login"""
    data = request.get_json()
    
    if not data or not data.get('google_id') or not data.get('email'):
        return jsonify({'message': 'Google ID and email are required'}), 400
    
    user = User.query.filter_by(google_id=data['google_id']).first()
    
    if not user:
        # Create new user from Google data
        user = User(
            username=data.get('name', data['email'].split('@')[0]),
            email=data['email'],
            google_id=data['google_id'],
            oauth_provider='google',
            is_active=True,
            email_verified=True
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return jsonify({
        'message': 'Google login successful',
        'user_id': user.id,
        'username': user.username
    }), 200

@auth_bp.route('/github-login', methods=['POST'])
def github_login():
    """GitHub OAuth login"""
    data = request.get_json()
    
    if not data or not data.get('github_id') or not data.get('login'):
        return jsonify({'message': 'GitHub ID and login are required'}), 400
    
    user = User.query.filter_by(github_id=data['github_id']).first()
    
    if not user:
        # Create new user from GitHub data
        user = User(
            username=data['login'],
            email=data.get('email', f"{data['login']}@github.local"),
            github_id=data['github_id'],
            oauth_provider='github',
            is_active=True,
            email_verified=True
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return jsonify({
        'message': 'GitHub login successful',
        'user_id': user.id,
        'username': user.username
    }), 200

@auth_bp.route('/link-oauth', methods=['POST'])
@login_required
def link_oauth():
    """Link OAuth provider to existing account"""
    data = request.get_json()
    
    if not data or not data.get('provider') or not data.get('provider_id'):
        return jsonify({'message': 'Provider and provider_id are required'}), 400
    
    provider = data['provider'].lower()
    
    if provider == 'google':
        current_user.google_id = data['provider_id']
    elif provider == 'github':
        current_user.github_id = data['provider_id']
    else:
        return jsonify({'message': 'Invalid provider'}), 400
    
    current_user.oauth_provider = provider
    db.session.commit()
    
    return jsonify({'message': f'{provider} account linked successfully'}), 200
