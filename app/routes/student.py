from flask import Blueprint, render_template, session, redirect, url_for

student = Blueprint('student', __name__)

@student.route('/student/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('student/dashboard.html')