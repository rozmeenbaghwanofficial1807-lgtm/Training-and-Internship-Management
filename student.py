from extensions import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    full_name = db.Column(db.String(140), nullable=False)
    phone = db.Column(db.String(25))
    college = db.Column(db.String(160))
    course = db.Column(db.String(120))
    skills = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    user = db.relationship("User", backref=db.backref("student_profile", uselist=False))
