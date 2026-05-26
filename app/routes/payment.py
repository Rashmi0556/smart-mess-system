from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db
from app.models import Payment, Subscription, Attendance, MealPlan, Student
from datetime import date

payment = Blueprint('payment', __name__)

def student_required():
    if 'user_id' not in session or session.get('user_role') != 'student':
        return redirect(url_for('auth.login'))
    return None

# ---------------------------------------------------------------
# BILL PAGE — shows calculated bill + payment history
# ---------------------------------------------------------------
@payment.route('/student/bill')
def bill():
    check = student_required()
    if check: return check

    std = Student.query.get(session['user_id'])

    # Get active subscription
    sub = Subscription.query.filter_by(
        student_id=std.student_id,
        status='active'
    ).first()

    total_bill = 0
    meals_eaten = 0

    if sub:
        plan = MealPlan.query.get(sub.plan_id)

        # Count meals eaten this month
        meals_eaten = Attendance.query.filter_by(
            student_id=std.student_id,
            mess_id=sub.mess_id,
            present=True
        ).filter(
            db.extract('month', Attendance.date) == date.today().month,
            db.extract('year',  Attendance.date) == date.today().year
        ).count()

        # Bill = meals eaten x per meal rate
        # per meal rate = plan price / total meals in plan (3 meals/day)
        total_meals_in_plan = plan.duration_days * 3
        if total_meals_in_plan > 0:
            per_meal = float(plan.price) / total_meals_in_plan
            total_bill = round(meals_eaten * per_meal, 2)

    # Get payment history
    payments = Payment.query.filter_by(
        student_id=std.student_id
    ).order_by(Payment.date.desc()).all()

    return render_template('payment/bill.html',
        student=std,
        subscription=sub,
        meals_eaten=meals_eaten,
        total_bill=total_bill,
        payments=payments
    )

# ---------------------------------------------------------------
# PAY — record a payment (atomic transaction)
# ---------------------------------------------------------------
@payment.route('/student/pay', methods=['POST'])
def pay():
    check = student_required()
    if check: return check

    std = Student.query.get(session['user_id'])
    amount = request.form.get('amount')
    method = request.form.get('method')

    try:
        # TRANSACTION — both operations succeed or both fail
        new_payment = Payment(
            student_id=std.student_id,
            amount=amount,
            date=date.today(),
            method=method,
            status='paid'
        )
        db.session.add(new_payment)
        db.session.commit()

        flash(f'Payment of ₹{amount} via {method} successful!', 'success')

    except Exception as e:
        db.session.rollback()  # undo everything if something fails
        flash('Payment failed. Please try again.', 'danger')

    return redirect(url_for('payment.bill'))