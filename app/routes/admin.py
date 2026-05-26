from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db
from app.models import MessAdmin, Subscription, Menu, Attendance, Student, MealPlan, Mess
from datetime import date

admin = Blueprint('admin', __name__)

def admin_required():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('auth.login'))
    return None

# ---------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------
@admin.route('/admin/dashboard')
def dashboard():
    check = admin_required()
    if check: return check

    adm = MessAdmin.query.get(session['user_id'])

    # Count active subscribers for this mess
    active_count = Subscription.query.filter_by(
        mess_id=adm.mess_id,
        status='active'
    ).count()

    # Count attendance marked today
    today_count = Attendance.query.filter_by(
        mess_id=adm.mess_id,
        date=date.today()
    ).count()

    return render_template('admin/dashboard.html',
        admin=adm,
        active_count=active_count,
        today_count=today_count,
        today=date.today()
    )

# ---------------------------------------------------------------
# SUBSCRIBERS LIST
# ---------------------------------------------------------------
@admin.route('/admin/subscribers')
def subscribers():
    check = admin_required()
    if check: return check

    adm = MessAdmin.query.get(session['user_id'])

    subs = db.session.query(Subscription, Student, MealPlan).join(
        Student, Subscription.student_id == Student.student_id
    ).join(
        MealPlan, Subscription.plan_id == MealPlan.plan_id
    ).filter(
        Subscription.mess_id == adm.mess_id,
        Subscription.status == 'active'
    ).all()

    return render_template('admin/subscribers.html', subs=subs)

# ---------------------------------------------------------------
# MENU EDITOR
# ---------------------------------------------------------------
@admin.route('/admin/menu', methods=['GET', 'POST'])
def menu_editor():
    check = admin_required()
    if check: return check

    adm = MessAdmin.query.get(session['user_id'])

    if request.method == 'POST':
        day       = request.form.get('day_of_week')
        meal_type = request.form.get('meal_type')
        items     = request.form.get('items')

        # Check if entry already exists for this day + meal_type
        existing = Menu.query.filter_by(
            mess_id=adm.mess_id,
            day_of_week=day,
            meal_type=meal_type
        ).first()

        if existing:
            existing.items = items  # update
        else:
            new_menu = Menu(
                mess_id=adm.mess_id,
                admin_id=adm.admin_id,
                day_of_week=day,
                meal_type=meal_type,
                items=items
            )
            db.session.add(new_menu)

        db.session.commit()
        flash('Menu updated successfully!', 'success')
        return redirect(url_for('admin.menu_editor'))

    # Get all existing menu entries for this mess
    menus = Menu.query.filter_by(mess_id=adm.mess_id).order_by(Menu.day_of_week).all()

    return render_template('admin/menu_editor.html', menus=menus)

# ---------------------------------------------------------------
# MARK ATTENDANCE
# ---------------------------------------------------------------
@admin.route('/admin/attendance', methods=['GET', 'POST'])
def mark_attendance():
    check = admin_required()
    if check: return check

    adm = MessAdmin.query.get(session['user_id'])

    if request.method == 'POST':
        # Get list of student_ids who were marked present
        present_ids = request.form.getlist('present')

        # Get all active subscribers for this mess
        all_subs = Subscription.query.filter_by(
            mess_id=adm.mess_id,
            status='active'
        ).all()

        for sub in all_subs:
            std = Student.query.get(sub.student_id)
            plan = MealPlan.query.get(sub.plan_id)

            # Check if attendance already marked today
            existing = Attendance.query.filter_by(
                student_id=sub.student_id,
                mess_id=adm.mess_id,
                date=date.today()
            ).first()

            is_present = str(sub.student_id) in present_ids

            if existing:
                existing.present = is_present
            else:
                att = Attendance(
                    student_id=sub.student_id,
                    mess_id=adm.mess_id,
                    date=date.today(),
                    meal_type=plan.meal_type,
                    present=is_present
                )
                db.session.add(att)

        db.session.commit()
        flash('Attendance marked for today!', 'success')
        return redirect(url_for('admin.mark_attendance'))

    # GET — show list of active subscribers
    subs = db.session.query(Subscription, Student).join(
        Student, Subscription.student_id == Student.student_id
    ).filter(
        Subscription.mess_id == adm.mess_id,
        Subscription.status == 'active'
    ).all()

    return render_template('admin/mark_attendance.html', subs=subs, today=date.today())