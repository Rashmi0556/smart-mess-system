from app import db, login_manager
from flask_login import UserMixin
from datetime import date

@login_manager.user_loader
def load_user(user_id):
    # Try student first, then admin
    user = Student.query.get(int(user_id))
    if not user:
        user = MessAdmin.query.get(int(user_id))
    return user

class Student(db.Model, UserMixin):
    __tablename__ = 'STUDENT'
    student_id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    room_no    = db.Column(db.String(10))
    email      = db.Column(db.String(100), unique=True, nullable=False)
    contact    = db.Column(db.String(15))
    password_hash = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.student_id)

class Mess(db.Model):
    __tablename__ = 'MESS'
    mess_id  = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)

class MessAdmin(db.Model, UserMixin):
    __tablename__ = 'MESS_ADMIN'
    admin_id      = db.Column(db.Integer, primary_key=True)
    mess_id       = db.Column(db.Integer, db.ForeignKey('MESS.mess_id'), nullable=False)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.admin_id)

class MealPlan(db.Model):
    __tablename__ = 'MEAL_PLAN'
    plan_id      = db.Column(db.Integer, primary_key=True)
    plan_name    = db.Column(db.String(100), nullable=False)
    price        = db.Column(db.Numeric(10,2), nullable=False)
    duration_days= db.Column(db.Integer, nullable=False)
    meal_type    = db.Column(db.Enum('veg','non-veg'), nullable=False)

class Subscription(db.Model):
    __tablename__ = 'SUBSCRIPTION'
    sub_id     = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('STUDENT.student_id'), nullable=False)
    mess_id    = db.Column(db.Integer, db.ForeignKey('MESS.mess_id'), nullable=False)
    plan_id    = db.Column(db.Integer, db.ForeignKey('MEAL_PLAN.plan_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date   = db.Column(db.Date, nullable=False)
    status     = db.Column(db.Enum('active','expired','cancelled'), default='active')

class Menu(db.Model):
    __tablename__ = 'MENU'
    menu_id    = db.Column(db.Integer, primary_key=True)
    mess_id    = db.Column(db.Integer, db.ForeignKey('MESS.mess_id'), nullable=False)
    admin_id   = db.Column(db.Integer, db.ForeignKey('MESS_ADMIN.admin_id'), nullable=False)
    day_of_week= db.Column(db.Enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), nullable=False)
    meal_type  = db.Column(db.Enum('veg','non-veg'), nullable=False)
    items      = db.Column(db.Text, nullable=False)

class Attendance(db.Model):
    __tablename__ = 'ATTENDANCE'
    att_id     = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('STUDENT.student_id'), nullable=False)
    mess_id    = db.Column(db.Integer, db.ForeignKey('MESS.mess_id'), nullable=False)
    date       = db.Column(db.Date, nullable=False)
    meal_type  = db.Column(db.Enum('veg','non-veg'), nullable=False)
    present    = db.Column(db.Boolean, default=False)

class Payment(db.Model):
    __tablename__ = 'PAYMENT'
    pay_id     = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('STUDENT.student_id'), nullable=False)
    amount     = db.Column(db.Numeric(10,2), nullable=False)
    date       = db.Column(db.Date, nullable=False, default=date.today)
    method     = db.Column(db.Enum('cash','UPI','card'), nullable=False)
    status     = db.Column(db.Enum('paid','pending','failed'), default='pending')