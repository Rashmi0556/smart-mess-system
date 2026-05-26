from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Student, MessAdmin

# What is a Blueprint?
# Instead of putting ALL routes in one file, Flask lets you split them into
# Blueprints. This file handles only auth routes (login, register, logout).
# Think of it like a chapter in a book — each Blueprint is one chapter.
auth = Blueprint('auth', __name__)


# ---------------------------------------------------------------
# REGISTER — create a new student account
# ---------------------------------------------------------------
# The route handles two situations:
#   GET  → user just opened the page, show them the form
#   POST → user submitted the form, process it
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # request.form is a dictionary of everything the user typed
        name     = request.form.get('name')
        email    = request.form.get('email')
        password = request.form.get('password')
        room_no  = request.form.get('room_no')
        contact  = request.form.get('contact')

        # Check if email already exists in DB
        existing = Student.query.filter_by(email=email).first()
        if existing:
            # flash() sends a one-time message to the next page
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password before saving — NEVER save plain text
        hashed_pw = generate_password_hash(password)

        # Create a new Student object (this is NOT saved yet)
        new_student = Student(
            name=name,
            email=email,
            password_hash=hashed_pw,
            room_no=room_no,
            contact=contact
        )

        # db.session.add() stages it, db.session.commit() actually saves to MySQL
        db.session.add(new_student)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    # GET request — just show the register form
    return render_template('auth/register.html')


# ---------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        role     = request.form.get('role')  # 'student' or 'admin'

        if role == 'student':
            user = Student.query.filter_by(email=email).first()
        else:
            user = MessAdmin.query.filter_by(email=email).first()

        # check_password_hash compares typed password with stored hash
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        # session is like a cookie Flask keeps on the server
        # We store who is logged in and what their role is
        session['user_id']   = user.student_id if role == 'student' else user.admin_id
        session['user_role'] = role
        session['user_name'] = user.name

        # Redirect to the right dashboard based on role
        if role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('admin.dashboard'))

    return render_template('auth/login.html')


# ---------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------
@auth.route('/logout')
def logout():
    # clear() removes everything from the session — user is now logged out
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))