from datetime import datetime
from extensions import db

class Internship(db.Model):
    __tablename__ = "internships"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(80))
    location = db.Column(db.String(120))
    stipend = db.Column(db.String(80))
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    company = db.relationship("Company", backref="internships")
