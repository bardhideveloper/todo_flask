from datetime import datetime
from flask import jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Task

def init_app(app):

    # -----------------------------
    # LOGIN & REGISTER ROUTES
    # -----------------------------
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            birthdate = request.form.get("birthdate")
            gender = request.form.get("gender")
            address = request.form.get("address")
            phone = request.form.get("phone")

            if User.query.filter_by(username=username).first():
                flash("Username already exists!")
                return redirect(url_for("register"))
            
            if User.query.filter_by(email=email).first():
                flash("Email already registered!")
                return redirect(url_for("register"))

            new_user = User(username=username, password=generate_password_hash(password),email=email,birthdate=birthdate,gender=gender,address=address,phone=phone)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created! You can now log in.")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                flash("Invalid username or password!")
                return redirect(url_for("login"))

            login_user(user)
            return redirect(url_for("index"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    # -----------------------------
    # TASK ROUTES
    # -----------------------------
    @app.route("/")
    @login_required
    def index():
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.order).all()
        return render_template("index.html", tasks=tasks)

    @app.route("/add", methods=["POST"])
    @login_required
    def add():
        task_text = request.form.get("task")
        deadline = request.form.get("deadline") or None
        priority = request.form.get("priority") or "Medium"
        

        if task_text:
            new_task = Task(task=task_text, user_id=current_user.id, deadline=deadline, priority=priority, created_by=current_user.username,created_at=datetime.utcnow())
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("index"))

    @app.route("/delete/<int:id>")
    @login_required
    def delete(id):
        task = Task.query.get(id)
        if task and task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for("index"))
    
    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit(id):
        task = Task.query.get(id)
        if not task or task.user_id != current_user.id:
            return jsonify({"error":"Unauthorized"}), 403

        if request.method == "POST":
            task.task = request.form.get("task")
            task.deadline = request.form.get("deadline") or None
            task.priority = request.form.get("priority")
            task.updated_by = current_user.username
            task.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({"success":True})

        return render_template("edit_form.html", task=task)

    @app.route("/complete/<int:id>")
    @login_required
    def complete(id):
        task = Task.query.get(id)
        if task and task.user_id == current_user.id:
            task.completed = not task.completed
            task.updated_by = current_user.username
            task.updated_at = datetime.utcnow()
            db.session.commit()
        return redirect(url_for("index"))

    @app.route("/toggle_theme")
    @login_required
    def toggle_theme():
        current_user.theme = "dark" if current_user.theme == "light" else "light"
        db.session.commit()
        return redirect(request.referrer or url_for("index"))

    @app.route("/reorder", methods=["POST"])
    @login_required
    def reorder():
        data = request.get_json() or []
        for item in data:
            task = Task.query.get(int(item.get('id')))
            if task and task.user_id == current_user.id:
                task.order = item.get('order', task.order)
                task.updated_by = current_user.username
                task.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"status": "ok"})
