from flask import Flask
from flask_login import LoginManager
from database import db
import os

def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Use Postgres database from Render
    # -----------------------------
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

    # Import routes
    import routes
    routes.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    return app

# -----------------------------
# Expose WSGI app for Gunicorn
# -----------------------------
app = create_app()  # <- Gunicorn should point to this 'app', not create_app()

# -----------------------------
# Local dev
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
