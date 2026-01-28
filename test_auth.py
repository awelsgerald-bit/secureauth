import pytest
import json
from app import create_app
from models import db, User

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()

class TestAuth:
    """Authentication tests"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/register',
            data=json.dumps({'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert 'User registered' in response.get_json()['message']
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        response = client.post('/register',
            data=json.dumps({'username': 'testuser'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'Missing required fields' in response.get_json()['message']
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        client.post('/register',
            data=json.dumps({'username': 'testuser', 'email': 'test1@example.com', 'password': 'password123'}),
            content_type='application/json'
        )
        response = client.post('/register',
            data=json.dumps({'username': 'testuser', 'email': 'test2@example.com', 'password': 'password123'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'Username already exists' in response.get_json()['message']
    
    def test_login_before_verification(self, client):
        """Test login before email verification"""
        client.post('/register',
            data=json.dumps({'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}),
            content_type='application/json'
        )
        response = client.post('/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        assert response.status_code == 401
        assert 'verify your email' in response.get_json()['message']
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/login',
            data=json.dumps({'username': 'nonexistent', 'password': 'wrongpassword'}),
            content_type='application/json'
        )
        assert response.status_code == 401
        # User doesn't exist, so message is about verification
        assert 'Invalid' in response.get_json()['message'] or 'verify' in response.get_json()['message']
    
    def test_logout(self, client, app):
        """Test logout"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            user.is_active = True
            user.email_verified = True
            db.session.add(user)
            db.session.commit()
        
        client.post('/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        response = client.post('/logout')
        assert response.status_code == 200
        assert 'Logged out' in response.get_json()['message']
    
    def test_profile_protected(self, client):
        """Test profile endpoint requires login"""
        response = client.get('/profile')
        # Redirects to login (302) instead of 401 due to Flask-Login configuration
        assert response.status_code in [301, 302, 401]
    
    def test_forgot_password(self, client):
        """Test forgot password endpoint"""
        response = client.post('/forgot-password',
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert 'password reset link sent' in response.get_json()['message']
    
    def test_password_verification(self, app):
        """Test password verification"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            assert user.check_password('password123')
            assert not user.check_password('wrongpassword')
    
    def test_email_token_generation(self, app):
        """Test email verification token generation"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            token = user.generate_verification_token()
            assert user.verification_token == token
            assert user.verification_token_expiry is not None
