import os
import uuid
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename   

from models import db, User
from forms import loginForm, EditProfileForm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max size
app.config['SECRET_KEY'] = 'devlink-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devlink.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user from the database when logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
        
@app.route('/', methods=['GET', 'POST'])
@login_required 
def profile():
    form = EditProfileForm(obj=current_user) # Pre-populate form with current user data
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.github = form.github.data
        current_user.tech_stack = form.tech_stack.data
        
        # Handle profile photo
        if form.profile_photo.data:
            file = form.profile_photo.data
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.root_path, 'static/uploads', unique_filename)
            file.save(file_path)
            current_user.profile_photo = unique_filename
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', form=form, user=current_user)
       
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Invalid login.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# Route for public profile view
@app.route('/u/<username>')
def public_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('public_profile.html', user=user)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed admin user if no users exist
        if not User.query.first():
            hashed_password = generate_password_hash('admin123')
            admin = User(username='admin', password=hashed_password)
            db.session.add(admin)
            db.session.commit()
            print("Admin user created (username: admin, password: admin123)")
    app.run(debug=True)