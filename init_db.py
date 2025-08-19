#!/usr/bin/env python3
from app import create_app
from app.models import db

# Create Flask application
app = create_app()

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
