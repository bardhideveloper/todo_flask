from app import create_app
from database import db

# Create app instance
app = create_app()

with app.app_context():
    # Drop all old tables
    db.drop_all()
    print("Old tables dropped!")

    # Recreate tables according to current models
    db.create_all()
    print("New tables created!")
