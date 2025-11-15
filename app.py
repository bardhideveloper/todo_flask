from flask import Flask
from flask_login import LoginManager
from database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "your_secret_key_here"

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from database import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    import routes
    routes.init_app(app)

    with app.app_context():
        db.create_all()

    return app

# Expose Flask instance for Gunicorn
app = create_app()

# Local development
if __name__ == "__main__":
    app.run(debug=True)
