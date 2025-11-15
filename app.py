from flask import Flask
from flask_login import LoginManager
from database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "your_secret_key_here"  # change this

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Import User model here to avoid circular imports
    from database import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes and register them
    import routes
    routes.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
