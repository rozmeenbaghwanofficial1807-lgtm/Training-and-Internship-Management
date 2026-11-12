from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models import User, Student, Company, Internship, Application, Notification
from .helpers import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@login_required
@role_required("Admin")
def dashboard():
    return render_template("admin/dashboard.html",
        student_count=Student.query.count(), company_count=Company.query.count(),
        internship_count=Internship.query.count(), application_count=Application.query.count(),
        pending_companies=Company.query.filter_by(approval_status="Pending").count(),
        pending_internships=Internship.query.filter_by(status="Pending").count())

@admin_bp.route("/students")
@login_required
@role_required("Admin")
def students():
    return render_template("admin/students.html", students=Student.query.order_by(Student.id.desc()).all())

@admin_bp.route("/companies")
@login_required
@role_required("Admin")
def companies():
    return render_template("admin/companies.html", companies=Company.query.order_by(Company.id.desc()).all())

@admin_bp.route("/company/<int:company_id>/approval", methods=["POST"])
@login_required
@role_required("Admin")
def company_approval(company_id):
    company = Company.query.get_or_404(company_id)
    status = request.form.get("status")
    if status not in {"Approved", "Rejected"}:
        flash("Invalid approval status.", "danger")
    else:
        company.approval_status = status
        db.session.add(Notification(user_id=company.user_id, title="Company account review",
                                    message=f"Your company account has been {status.lower()}."))
        db.session.commit()
        flash(f"Company {status.lower()}.", "success")
    return redirect(url_for("admin.companies"))

@admin_bp.route("/internships")
@login_required
@role_required("Admin")
def internships():
    return render_template("admin/internships.html", internships=Internship.query.order_by(Internship.id.desc()).all())

@admin_bp.route("/internship/<int:internship_id>/approval", methods=["POST"])
@login_required
@role_required("Admin")
def internship_approval(internship_id):
    item = Internship.query.get_or_404(internship_id)
    status = request.form.get("status")
    if status not in {"Approved", "Rejected", "Closed"}:
        flash("Invalid internship status.", "danger")
    else:
        item.status = status
        item.approved_by = __import__("flask_login").current_user.id
        db.session.add(Notification(user_id=item.company.user_id, title="Internship review",
                                    message=f"Your internship '{item.title}' has been {status.lower()}."))
        db.session.commit()
        flash(f"Internship {status.lower()}.", "success")
    return redirect(url_for("admin.internships"))

@admin_bp.route("/applications")
@login_required
@role_required("Admin")
def applications():
    return render_template("admin/applications.html", applications=Application.query.order_by(Application.applied_at.desc()).all())
