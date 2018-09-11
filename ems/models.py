from datetime import datetime
from ems import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    j_date = db.Column(db.DateTime, nullable=False,
                       default=datetime.utcnow)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(70), nullable=True)
    salary = db.Column(db.String(15), nullable=False)
    designation = db.Column(db.String(30), nullable=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default_emp.svg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Employee('{self.emp_id}', '{self.name}', '{self.salary}', '{self.designation}', '{self.user_id}')"
