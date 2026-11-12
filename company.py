from extensions import db

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    company_name = db.Column(db.String(160), nullable=False)
    contact_person = db.Column(db.String(120))
    phone = db.Column(db.String(25))
    address = db.Column(db.String(255))
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default="Pending", nullable=False)
    user = db.relationship("User", backref=db.backref("company_profile", uselist=False))
