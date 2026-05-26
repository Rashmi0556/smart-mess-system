from flask import Blueprint, render_template, session, redirect, url_for

payment = Blueprint('payment', __name__)

@payment.route('/student/bill')
def bill():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('payment/bill.html')