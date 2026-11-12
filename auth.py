from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Student, Company

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "Student")
        if not name or not email or len(password) < 8 or role not in ("Student", "Company"):
            flash("Complete all fields. Password must contain at least 8 characters.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("That email address is already registered.", "danger")
        else:
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            if role == "Student":
                db.session.add(Student(user_id=user.id, full_name=name))
            else:
                db.session.add(Company(user_id=user.id, company_name=name, contact_person=name))
            db.session.commit()
            flash("Registration successful. Sign in to continue.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid email/password or inactive account.", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))
