from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db
from app.models import Student, Subscription, MealPlan, Mess, Menu, Attendance
from datetime import date

student = Blueprint('student', __name__)

# Helper — blocks page if not logged in as student
def student_required():
    if 'user_id' not in session or session.get('user_role') != 'student':
        return redirect(url_for('auth.login'))
    return None

# ---------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------
@student.route('/student/dashboard')
def dashboard():
    check = student_required()
    if check: return check

    # Get the logged in student from DB
    std = Student.query.get(session['user_id'])

    # Get their active subscription if any
    sub = Subscription.query.filter_by(
        student_id=std.student_id,
        status='active'
    ).first()

    # Count meals eaten this month
    meals_eaten = 0
    if sub:
        meals_eaten = Attendance.query.filter_by(
            student_id=std.student_id,
            present=True
        ).filter(
            db.extract('month', Attendance.date) == date.today().month,
            db.extract('year',  Attendance.date) == date.today().year
        ).count()

    return render_template('student/dashboard.html',
        student=std,
        subscription=sub,
        meals_eaten=meals_eaten,
        today=date.today()
    )

# ---------------------------------------------------------------
# TODAY'S MENU
# ---------------------------------------------------------------
@student.route('/student/menu')
def menu():
    check = student_required()
    if check: return check

    std = Student.query.get(session['user_id'])

    # Get active subscription to know their meal_type (veg/non-veg)
    sub = Subscription.query.filter_by(
        student_id=std.student_id,
        status='active'
    ).first()

    menu_items = None
    if sub:
        plan = MealPlan.query.get(sub.plan_id)
        today_name = date.today().strftime('%A')  # e.g. "Monday"

        # Fetch menu matching their mess + day + meal_type
        menu_items = Menu.query.filter_by(
            mess_id=sub.mess_id,
            day_of_week=today_name,
            meal_type=plan.meal_type
        ).first()

    return render_template('student/menu.html',
        menu=menu_items,
        subscription=sub
    )

# ---------------------------------------------------------------
# SUBSCRIPTION — choose mess and plan
# ---------------------------------------------------------------
@student.route('/student/subscription', methods=['GET', 'POST'])
def subscription():
    check = student_required()
    if check: return check

    std = Student.query.get(session['user_id'])
    active_sub = Subscription.query.filter_by(
        student_id=std.student_id,
        status='active'
    ).first()

    if request.method == 'POST':
        mess_id  = request.form.get('mess_id')
        plan_id  = request.form.get('plan_id')
        start    = date.today()

        plan = MealPlan.query.get(plan_id)
        from datetime import timedelta
        end = start + timedelta(days=plan.duration_days)

        # Cancel any existing subscription first
        if active_sub:
            active_sub.status = 'cancelled'

        new_sub = Subscription(
            student_id=std.student_id,
            mess_id=mess_id,
            plan_id=plan_id,
            start_date=start,
            end_date=end,
            status='active'
        )
        db.session.add(new_sub)
        db.session.commit()

        flash('Subscription activated!', 'success')
        return redirect(url_for('student.dashboard'))

    # GET — show all available messes and plans
    messes = Mess.query.all()
    plans  = MealPlan.query.all()

    return render_template('student/subscription.html',
        messes=messes,
        plans=plans,
        active_sub=active_sub
    )

# ---------------------------------------------------------------
# ATTENDANCE HISTORY
# ---------------------------------------------------------------
@student.route('/student/attendance')
def attendance():
    check = student_required()
    if check: return check

    std = Student.query.get(session['user_id'])

    # Get last 30 attendance records
    records = Attendance.query.filter_by(
        student_id=std.student_id
    ).order_by(Attendance.date.desc()).limit(30).all()

    return render_template('student/attendance.html',
        records=records,
        student=std
    )