import os
from flask import Flask
from flask_login import LoginManager
from database import db
import routes

def get_database_url():
    # Use DATABASE_URL from Render or fallback to local SQLite
    return os.environ.get("DATABASE_URL", "sqlite:///todo.db")

# -----------------------------
# Create Flask app
# -----------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your_secret_key_here")

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Import User model to avoid circular imports
from database import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register routes
routes.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# -----------------------------
# Local development
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
