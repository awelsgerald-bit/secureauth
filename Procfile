web: gunicorn -w 1 -b 0.0.0.0:$PORT app:create_app()
release: python -c "from app import create_app, db; app = create_app(); db.create_all()"
