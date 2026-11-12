from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from models import Internship, Application, Student, Company

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    internships = Internship.query.filter_by(status="Approved").order_by(Internship.created_at.desc()).limit(6).all()
    return render_template("index.html", internships=internships)

@main_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "Admin":
        return redirect(url_for("admin.dashboard"))
    if current_user.role == "Student":
        profile = Student.query.filter_by(user_id=current_user.id).first()
        applications = Application.query.filter_by(student_id=profile.id).order_by(Application.applied_at.desc()).limit(5).all() if profile else []
        return render_template("student/dashboard.html", profile=profile, applications=applications,
                               internship_count=Internship.query.filter_by(status="Approved").count())
    profile = Company.query.filter_by(user_id=current_user.id).first()
    internships = Internship.query.filter_by(company_id=profile.id).all() if profile else []
    return render_template("company/dashboard.html", profile=profile, internships=internships)
