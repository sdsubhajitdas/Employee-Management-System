import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from ems import app, bcrypt, db
from ems.forms import RegistrationForm, LoginForm, AccountForm, AddNewForm, UpdateDetailsForm
from ems.models import User, Employee


@app.route("/")
@app.route("/index")
@app.route("/home")
@login_required
def home():
    emps = Employee.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', emps=emps, title="Employee Management System")


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hash_pass)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Your account has been created.You are now able to log in !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful for {user.username} !', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email & password', 'danger')

    return render_template('login.html', title="Sign In", form=form)


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    logout_user()
    flash(f'Logout Successful.', 'success')
    return redirect(url_for('home'))


def save_picture(picture_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_data.filename)
    pic_name = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_images', pic_name)
    picture_data.save(pic_path)
    return pic_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_url = url_for('static', filename=str(
        'profile_images/'+current_user.image_file))
    username = current_user.username
    email = current_user.email
    form = AccountForm()
    if request.method == 'POST':
        # if form.validate_on_submit():
        if form.dp.data:
            img_file = current_user.image_file
            if 'default' not in img_file:
                if os.path.exists('ems/static/profile_images/'+img_file):
                    os.remove('ems/static/profile_images/'+img_file)
                    print(f'Pic deleted\nems/static/profile_images/{img_file}')
                else:
                    print("Picture not deleted")
            name = save_picture(form.dp.data)
            current_user.image_file = name

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash(f'Account Updated', 'info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.gender.data = '' if current_user.gender == None else current_user.gender

    return render_template('account.html', title="Account", form=form,
                           image_url=image_url, username=username, email=email)


@app.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = AddNewForm()
    if form.validate_on_submit():
        emp = None
        if form.dp.data:
            name = save_picture(form.dp.data)
            emp = Employee(emp_id=form.emp_id.data,
                           name=form.name.data,
                           address=form.address.data,
                           phone=form.phone.data,
                           email=form.email.data,
                           salary=form.salary.data,
                           designation=form.designation.data,
                           image_file=name,
                           user_id=current_user.id)
        else:
            emp = Employee(emp_id=form.emp_id.data,
                           name=form.name.data,
                           address=form.address.data,
                           phone=form.phone.data,
                           email=form.email.data,
                           salary=form.salary.data,
                           designation=form.designation.data,
                           user_id=current_user.id)
        db.session.add(emp)
        db.session.commit()
        flash('New Employee has been added', 'success')
        return redirect(url_for('home'))
    return render_template('new.html', title="Add New Employee", form=form)


@app.route("/update/<int:emp_p_id>", methods=['GET', 'POST'])
@login_required
def update(emp_p_id):
    emp = Employee.query.get(emp_p_id)
    form = UpdateDetailsForm()
    if emp.user_id == current_user.id:
        dp_url = emp.image_file
        form.old_id.data = emp.emp_id
        if form.validate_on_submit():
            if form.dp.data:
                old_filename = emp.image_file
                if old_filename != 'default_emp.svg':
                    if os.path.exists('ems/static/profile_images/'+old_filename):
                        os.remove('ems/static/profile_images/'+old_filename)
                        print(
                            f'Pic deleted\nems/static/profile_images/{old_filename}')
                    else:
                        print("Picture not deleted")
                new_name = save_picture(form.dp.data)
                emp.image_file = new_name

            emp.emp_id = form.emp_id.data
            emp.name = form.name.data
            emp.address = form.address.data
            emp.phone = form.phone.data
            emp.email = form.email.data
            emp.salary = form.salary.data
            emp.designation = form.designation.data
            db.session.commit()
            flash("Employee Details Updated", 'success')
            return redirect('home')

        elif request.method == 'GET':
            form.emp_id.data = emp.emp_id
            form.name.data = emp.name
            form.address.data = emp.address
            form.phone.data = emp.phone
            form.email.data = emp.email
            form.salary.data = emp.salary
            form.designation.data = emp.designation

    else:
        flash('You are not authorized to edit this employee details', 'danger')
        return redirect('home')
    return render_template('update_emp.html', title="Update Employee Details", form=form, dp_url=dp_url)


@app.route("/delete/<int:emp_p_id>")
@login_required
def delete(emp_p_id):
    emp = Employee.query.get(emp_p_id)
    if emp.user_id == current_user.id:
        name = emp.name
        img_file = emp.image_file
        db.session.delete(emp)
        db.session.commit()
        if img_file != 'default_emp.svg':
            if os.path.exists('ems/static/profile_images/'+img_file):
                os.remove('ems/static/profile_images/'+img_file)
                print(f'Pic deleted\nems/static/profile_images/{img_file}')
            else:
                print("Picture not deleted")
        flash(f'{name} deleted successfully', 'success')
    else:
        flash('You are not authorized to delete this employee details', 'danger')
    return redirect('home')
