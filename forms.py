# from collections.abc import Sequence
# from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from models import AdminUser,Users
from werkzeug.security import check_password_hash
from flask import session
class UserSignUpForm(FlaskForm):
    user_name = StringField("Name",validators=[DataRequired("Please Enter Username")],render_kw={"class": "form-control"})
    user_phone_number = IntegerField("Phone Number",validators=[DataRequired("Please Enter Phone Number")],render_kw={"class": "form-control"})
    user_email_address = StringField("Email Address",validators=[DataRequired("Please Enter Email Address"),Email("email should be correct")],render_kw={"class": "form-control"})
    user_password = PasswordField("Password",validators=[DataRequired("Please Enter Password"),Length(min=6,max=14)],render_kw={"class": "form-control"})
    user_confirm_password = PasswordField("Confirm Password",validators=[DataRequired("Please Enter Password"),EqualTo("user_password","Confirm Password Must Be Same to Password")],render_kw={"class": "form-control"})
    signup = SubmitField("Sign In",render_kw={"class": "btn"})

    def validate_user_email_address(self,user_email_address):
        emailcheck = Users.query.filter(Users.user_email_address == user_email_address.data).first()
        admin_data=AdminUser.query.filter(AdminUser.admin_email_address == user_email_address.data).first()
        if admin_data:
            raise ValidationError("Emails Is Already Registered")
        if emailcheck:
            raise ValidationError("Emails Is Already Registered")
        
    def validate_user_phone_number(self,user_phone_number):
        phonecheck = Users.query.filter(Users.user_phone_number == user_phone_number.data).first()
        if phonecheck:
            raise ValidationError("Phone Number Is Already Registered")
        phonecheck = AdminUser.query.filter(AdminUser.admin_phone_number == user_phone_number.data).first()
        if phonecheck:
            raise ValidationError("Phone Number Is Already Registered")

class UserSignInForm(FlaskForm):
    user_email_address = StringField("Email Address",validators=[DataRequired("Please Enter Email Address"),Email("email should be correct")],render_kw={"class": "form-control"})
    user_password = PasswordField("Password",validators=[DataRequired("Please Enter Password")],render_kw={"class": "form-control"})
    signin = SubmitField("Sign In",render_kw={"class": "btn"})

class ProfileDetails(FlaskForm):
    name = StringField("Name",validators=[DataRequired("Please Enter Name")])
    phone_number = IntegerField("Phone Number",validators=[DataRequired("Please Enter Phone Number")])
    save = SubmitField("Save")

    def validate_phone_number(self,phone_number):
        from flask_login import current_user    
        phone=Users.query.filter(Users.id!=current_user.id and Users.user_phone_number==phone_number.data).first()
        if phone:
            raise ValidationError("Phone Number is already registered with some other account, so two accounts cant have same number")

class ProfilePasswords(FlaskForm):
    current_password = PasswordField("Current Password",validators=[DataRequired("Please Enter Current Password"),Length(min=6,max=14)])
    new_password = PasswordField("New Password",validators=[DataRequired("Please Enter New Password"),Length(min=6,max=14)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            EqualTo("new_password","Confirm Password Must Be Same to New Password")
        ]
    )
    save = SubmitField("Save")

    def validate_current_password(self,current_password):
        from flask_login import current_user    
        pwhash=Users.query.filter(Users.id==current_user.id).first()
        if pwhash:
            pwhash=pwhash.user_password
        else:
            pwhash=AdminUser.query.filter(AdminUser.id==current_user.id).first()
            pwhash=pwhash.admin_password

        if check_password_hash(pwhash=pwhash,password=current_password.data):
            raise ValidationError("Current Password Does Not match")
            
class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()],render_kw={"class": "form-control"})
    description = TextAreaField('Description', validators=[DataRequired()],render_kw={"class": "form-control"})
    price = IntegerField('Price', validators=[DataRequired()],render_kw={"class": "form-control"})
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()],render_kw={"class": "form-control"})
    submit = SubmitField('Save')

class BookingForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired("Please Enter Username")])
    email_address = StringField("Email Address",validators=[DataRequired("Please Enter Email Address"),Email("email should be correct")])
    phone_number = IntegerField("Phone Number",validators=[DataRequired("Please Enter Phone Number")])
    date = DateField('Date', format="%Y-%m-%d", validators=[DataRequired()])
    time = SelectField("Time",choices=[f"{i}:00" for i in range(9,21)])
    submit = SubmitField('Book')   

    def validate_email_address(self,email_address):
        if not session.get('user_type'):
            emailcheck = Users.query.filter(Users.user_email_address == email_address.data).first()
            admin_data=AdminUser.query.filter(AdminUser.admin_email_address == email_address.data).first()
            if admin_data:
                raise ValidationError("Email account is registered with us, Please Login to booking")
            if emailcheck:
                raise ValidationError("Email account is registered with us, Please Login to booking")
        
    def validate_phone_number(self,phone_number):
        if not session.get('user_type'):
            phonecheck = Users.query.filter(Users.user_phone_number == phone_number.data).first()
            if phonecheck:
                raise ValidationError("Phone Number is registered with us, Please Login to booking")
            phonecheck = AdminUser.query.filter(AdminUser.admin_phone_number == phone_number.data).first()
            if phonecheck:
                raise ValidationError("Phone Number is registered with us, Please Login to booking")