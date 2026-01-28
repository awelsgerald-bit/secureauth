from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from models import db, User

migrate = Migrate()
mail = Mail()

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from routes import auth_bp
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def index():
        return {'message': 'Flask Authentication System', 'version': '1.0'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
