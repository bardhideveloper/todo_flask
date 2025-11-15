import os
from flask import Flask
from flask_login import LoginManager
from database import db

def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Configuration
    # -----------------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///todo.db"
    )
    # For Postgres on Render, DATABASE_URL is automatically provided
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret_key")

    # -----------------------------
    # Initialize extensions
    # -----------------------------
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # -----------------------------
    # User loader
    # -----------------------------
    from database import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # -----------------------------
    # Register routes
    # -----------------------------
    import routes
    routes.init_app(app)

    # -----------------------------
    # Create tables if they don't exist
    # -----------------------------
    with app.app_context():
        db.create_all()

    return app


# -----------------------------
# Expose WSGI app for Gunicorn
# -----------------------------
app = create_app()

# -----------------------------
# Local development
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
