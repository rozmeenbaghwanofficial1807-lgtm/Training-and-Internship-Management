from datetime import datetime
from extensions import db

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable=False)
    resume_path = db.Column(db.String(255))
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(20), default="Applied", nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    student = db.relationship("Student", backref="applications")
    internship = db.relationship("Internship", backref="applications")
    __table_args__ = (db.UniqueConstraint("student_id", "internship_id", name="unique_student_internship"),)
