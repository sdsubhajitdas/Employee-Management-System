from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ems.models import User, Employee
from sqlalchemy import and_
from ems import db


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email is already registered. Please sign in to your existing account.')


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In')


class AccountForm(FlaskForm):
    username = StringField("Username",)
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    gender = SelectField(choices=[('0', ''), ('1', 'male'), ('2', 'female')])
    dp = FileField("Upload New Display Picture")
    update = SubmitField('Update Information')


class EmpDetailsForm (FlaskForm):
    emp_id = StringField("Employee Id", validators=[
                         Length(min=1, max=10), DataRequired()])
    name = StringField("Employee Name", validators=[
                       Length(min=5), DataRequired()])
    address = StringField("Employee Address")
    phone = StringField("Employee Contact Number")
    email = StringField("Employee Email ID", validators=[Email()])
    salary = StringField("Employee Salary", validators=[
                         Length(min=3), DataRequired()])
    designation = StringField("Employee Designation")
    #j_date = DateField("Employee Joining Date", format='%d-%m-%Y')
    dp = FileField("Display Picture For Employee")


class AddNewForm(EmpDetailsForm):
    submit = SubmitField('Add New Employee')

    def validate_emp_id(self, emp_id):
        emp = Employee.query.filter(Employee.user_id == current_user.id).filter(
            Employee.emp_id == emp_id.data).first()
        if emp:
            raise ValidationError(
                'This employee ID is already registered in the database.')


class UpdateDetailsForm(EmpDetailsForm):
    old_id = StringField("Old Id")
    submit = SubmitField("Update Employee Details")
    def validate_emp_id(self,emp_id):
        if emp_id.data != self.old_id.data:
            emp = Employee.query.filter(Employee.user_id == current_user.id).filter(
                Employee.emp_id == emp_id.data).first()
            if emp:
                raise ValidationError(
                    'This employee ID is already registered in the database.')
