from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import bcrypt
from models import User

def register(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
            
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            try:
                user = User.query.filter_by(username=username).first()
                if user and bcrypt.check_password_hash(user.password_hash, password):
                    login_user(user)
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Login Unsuccessful. Please check credentials.', 'error')
            except Exception as e:
                flash('An unexpected system error occurred.', 'error')
                
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))