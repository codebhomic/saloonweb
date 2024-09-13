from flask import (
    Flask,Blueprint, flash, redirect, render_template, request, session, url_for,abort
)
from forms import UserSignInForm,UserSignUpForm,ProfilePasswords,ProfileDetails
from dbase import db
from models import Users,AdminUser,Clients
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
users = Blueprint('users', __name__, url_prefix='/users')
# def only_user(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_type") != None and session.get('user_type') == 'admin':
#             flash("You do not have permission to access this page.", "error")
#             return redirect(url_for('admin.admin_mainpage'))
#         return f(*args, **kwargs)
#     return decorated_function

@users.route('/profile')
@login_required
# @only_user
def profile():
    if session.get('user_type') != 'user':
        return redirect(url_for('admin.admin_mainpage'))
    return render_template('admin/profile.html',isadmin=False)

@users.route("/settings/change-password",methods=["GET", "POST"])
@login_required 
# @only_user
def profile_change_password():
    form = ProfilePasswords()
    if form.validate_on_submit():
        adminupdate = Users.query.filter(Users.id==current_user.id).first()
        adminupdate.user_password=generate_password_hash(form.new_password.data)
        db.session.commit()
        flash("Password Updated.....",'success')
        return redirect(url_for('users.profile'))
    return render_template("users/settings.html",form=form,type="change_password")

@users.route("/settings/change-profile-details",methods=["GET", "POST"])
@login_required 
# @only_user
def profile_details():
    form = ProfileDetails()
    if form.validate_on_submit():
        try:
            userupdate = Users.query.filter(Users.id==current_user.id).first()
            userupdate.user_name=form.name.data
            userupdate.user_phone_number=form.phone_number.data
            db.session.commit()
            flash("Details Updated.....",'success')
            return redirect(url_for('users.profile'))
        except Exception as err:
            flash("Phone Number is already registered by some user please check details",'error')
            return redirect(url_for('users.profile'))

    return render_template("users/settings.html",form=form,type="profile_details")

@users.route('/sign-in', methods=['GET', 'POST'])
# @only_user
def signin():
    if session.get("user_type") != None and session.get('user_type') == 'user':
        return redirect(url_for("users.profile"))
    page = request.args.get("next","/admin/")
    form = UserSignInForm()
    if form.validate_on_submit():
        admin_data=AdminUser.query.filter(AdminUser.admin_email_address == form.user_email_address.data).first()
        user_check=Users.query.filter(Users.user_email_address == form.user_email_address.data).first()
        if admin_data:
            if check_password_hash(admin_data.admin_password, form.user_password.data):
                login_user(admin_data)
                session['user_type'] = 'admin'
                flash(f"{admin_data.admin_name}, You have Logged IN!!","success")
                if "admin" in page:
                    return redirect(page)
                return redirect(url_for('admin.admin_mainpage'))
        if user_check:
            if check_password_hash(user_check.user_password, form.user_password.data):
                login_user(user_check)
                session['user_type'] = 'user'
                flash("You have Logged IN!!","success")
                return redirect(url_for('users.profile'))     
        flash("No Account Found, please Create account or enter valid details","error")
    register = False
    return render_template('users/signin.html',register=register,form=form)

@users.route('/sign-up', methods=['GET', 'POST'])
# @login_required
def signup():
    if session.get("user_type") != None:
        return redirect(url_for("users.profile"))
    form = UserSignUpForm()
    if form.validate_on_submit():
        user_check=Users.query.filter(Users.user_email_address == form.user_email_address.data).first()
        phonecheck = Users.query.filter(Users.user_phone_number == form.user_email_address.data).first()
        if not user_check and not phonecheck:
            users_signin = Users(
        user_name = form.user_name.data,
        user_phone_number = form.user_phone_number.data,
        user_email_address = form.user_email_address.data,
        user_password = generate_password_hash(form.user_password.data)
            )
            db.session.add(users_signin)
            db.session.commit()
            userid = Users.query.filter(Users.user_email_address==form.user_email_address.data).first()
            if not userid:
                return "Internal Server Error"
            clientid=Clients.query.filter(Clients.email_address==form.user_email_address.data).first()
            if clientid:
                from models import Bookings
                bookid = Bookings.query.filter(Bookings.client_id==clientid.id).first()
                if bookid:
                    bookid.user_id=userid.id
                    bookid.client_id=""
                    db.session.commit()
            flash("You Can Login Your Account is created","success")
            return redirect(url_for("users.signin"))
    register = True
    return render_template('users/signin.html',register=register,form=form)
    
@users.route('/sign-out')
@login_required
# @only_user
def logout():
    logout_user()
    session.pop("user_type",None)
    flash("You Have Successfully LogOut","success")
    return redirect(url_for("users.signin"))