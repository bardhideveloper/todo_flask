from flask import Flask
from flask_login import LoginManager
from database import db

def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Use Postgres database from Render
    # Set this as an environment variable in Render: DATABASE_URL
    # Example: postgres://username:password@hostname:port/dbname
    # -----------------------------
    import os
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///todo.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bardhiyllka")

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # User loader
    from database import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes and register
    import routes
    routes.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

# -----------------------------
# Expose Flask app instance for Gunicorn
# -----------------------------
app = create_app()

# -----------------------------
# Local development
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
