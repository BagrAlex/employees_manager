from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from employees_manager.database.models import User, db, SystemSettings
from .forms import LoginForm, RegistrationForm
from .utils import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print('user-pass',username, password)
        user = User.query.filter_by(username=username).first()
        if user and verify_password(user.password_hash, password):
            print('here')
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Неправльный логин или пароль', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Проверяем, включена ли регистрация
    registration_enabled = SystemSettings.get_setting('registration_enabled', 'True') == 'True'
    if not registration_enabled:
        flash('Registration is currently disabled.', 'warning')
        return redirect(url_for('auth.login'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = hash_password(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Registration is failed.', 'warning')
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))