from pathlib import Path
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, migrate
from models import User
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from routes.student import student_bp
from routes.company import company_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("error.html", code=403, message="You do not have permission to access this page."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", code=404, message="The page you requested could not be found."), 404

    @app.errorhandler(413)
    def too_large(error):
        return render_template("error.html", code=413, message="File too large. Maximum upload size is 5 MB."), 413

    with app.app_context():
        db.create_all()
        create_default_admin()

    return app

def create_default_admin():
    import os
    email = os.getenv("ADMIN_EMAIL", "admin@example.com").strip().lower()
    if not User.query.filter_by(email=email).first():
        admin = User(name=os.getenv("ADMIN_NAME", "System Administrator"), email=email, role="Admin")
        admin.set_password(os.getenv("ADMIN_PASSWORD", "ChangeThisAdminPassword123!"))
        db.session.add(admin)
        db.session.commit()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
