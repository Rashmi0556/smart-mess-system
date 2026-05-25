from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Student, MessAdmin

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name      = request.form.get('name')
        email     = request.form.get('email')
        password  = request.form.get('password')
        room_no   = request.form.get('room_no')
        contact   = request.form.get('contact')

        existing = Student.query.filter_by(email=email).first()
        if existing:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        new_student = Student(
            name=name,
            email=email,
            password_hash=hashed_pw,
            room_no=room_no,
            contact=contact
        )
        db.session.add(new_student)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        role     = request.form.get('role')

        if role == 'student':
            user = Student.query.filter_by(email=email).first()
        else:
            user = MessAdmin.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id']   = user.student_id if role == 'student' else user.admin_id
        session['user_role'] = role
        session['user_name'] = user.name

        if role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('admin.dashboard'))

    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))