from flask import (
Blueprint, render_template, abort, redirect, render_template, request, session, url_for,flash
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from dbase import db
from models import *
from functools import wraps
from flask import session, redirect, url_for, flash
from forms import *
from json import dumps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'admin':
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Custom 404 error handler
@admin.app_errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404

@admin.route("/")
@login_required
@admin_required
def admin_mainpage():
    # return redirect(url_for("admin.profile"))
    return render_template("admin/mainpage.html", admin_name="")

@admin.route("/login", methods=["GET"])
def admin_login():
    page = request.args.get("next","/admin/")
    return render_template("admin/login.html",page=page)

@admin.route("/loginsubmit", methods=["GET", "POST"])
def admin_login_submit():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        page = request.form['page']
        error = None
        admin_data = AdminUser.query.filter(AdminUser.admin_email_address == email).first()
        try:
            if not check_password_hash(admin_data.admin_password, password):
                error = 'Incorrect password.'
        except Exception as err:
            error = f"email address not found"
        if error is None:
            login_user(admin_data)
            session['user_type'] = 'admin'
            flash("You have Logged IN!!","success")
            if "admin" in page:
                return redirect(page)
            return redirect(url_for('admin.admin_mainpage'))
        flash(error,"error")
        return redirect(url_for('admin.admin_login'))
    else:
        return abort(404)
    
@admin.route("/logout")
@login_required
@admin_required
def admin_logout():
    logout_user()
    session.pop('user_type', None)
    flash("You Have Successfully LogOut","success")
    return redirect(url_for("admin.admin_login"))

@admin.route("/profile")
@login_required
@admin_required
def profile():
    isadmin=True
    return render_template("admin/profile.html",isadmin=isadmin)

@admin.route("/profile/change-password",methods=["GET", "POST"])
@login_required
@admin_required
def profile_change_password():
    form = ProfilePasswords()
    if form.validate_on_submit():
        adminupdate = AdminUser.query.filter(AdminUser.id==current_user.id).first()
        adminupdate.admin_password=generate_password_hash(form.new_password.data)
        db.session.commit()
        flash("Password Updated.....",'success')
        return redirect(url_for('admin.profile'))
    return render_template("admin/settings.html",form=form,type="change_password")

@admin.route("/profile/change-profile-details",methods=["GET", "POST"])
@login_required
@admin_required
def profile_details():
    form = ProfileDetails()
    if form.validate_on_submit():
        adminupdate = AdminUser.query.filter(AdminUser.id==current_user.id).first()
        adminupdate.admin_name=form.name.data
        adminupdate.admin_phone_number=form.phone_number.data
        db.session.commit()
        flash("Details Updated.....",'success')
        return redirect(url_for('admin.profile'))
    return render_template("admin/settings.html",form=form,type="profile_details")

@admin.route("/getcontact")
@login_required
@admin_required
def getcontact():
    page = request.args.get('page', 1, type=int)
    allcontact = ContactUs.query.paginate(page=page,per_page=10,error_out=False)
    return render_template("admin/getcontact.html",contacts=allcontact)

@admin.route("/deletecontact/<id>")
@admin_required
def deletecontact(id):
    contactid = ContactUs.query.filter(ContactUs.id == id).first()
    if contactid and not contactid == None:
        db.session.delete(contactid)
        db.session.commit()
        flash("Contact Deleted","success")
    else:
        flash("Contact Not Found to be Deleted","error")
    return redirect(url_for("admin.getcontact"))


@admin.route("/admin_create")
@login_required
@admin_required
def admin_create():
    # adminsubmit = AdminUser(
    # admin_name = "admin",
    # admin_phone_number = "9999999",
    # admin_email_address = "admin@gmail.com",
    # admin_password = generate_password_hash("admin1234")
    #     )
    # db.session.add(adminsubmit)
    # db.session.commit()
    return "success"

@admin.route("/booking/details", methods=["GET"])
@login_required
@admin_required
def booking_details():
    page = request.args.get('page', 1, type=int)
    typeof = request.args.get('type')
    bookinginfo = Bookings.query.paginate(page=page,per_page=10,error_out=False)
    if typeof and typeof == "client":
        bookinginfo = Bookings.query.filter(
            Bookings.client_id != "" or Bookings.user_id == ""
            ).paginate(page=page,per_page=10,error_out=False)
    elif typeof and typeof=='user':
        bookinginfo = Bookings.query.filter(Bookings.user_id != "").paginate(page=page,per_page=10,error_out=False)
    services = Services.query.all()
    # return dumps(bookinginfo.items)
    return render_template('admin/bookingdetails.html',binfo=bookinginfo,serv=services,typeof=typeof)


@admin.route("/booking/delete/<int:id>")
@admin_required
def deletebooking(id):
    booking = Bookings.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking Detail Deleted","success")
    return redirect(url_for("admin.booking_details"))


@admin.route("/services/view")
@login_required
@admin_required
def view_services():
    page = request.args.get('page', 1, type=int)
    servicesdata = Services.query.paginate(page=page,per_page=10,error_out=False)
    return render_template("admin/view_services.html",services=servicesdata)

@admin.route("/services/add",methods=["GET", "POST"])
@login_required
@admin_required
def add_services():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Services(title=form.name.data, desc=form.description.data, price=form.price.data, duration=form.duration.data)
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully',"success")
        return redirect(url_for('admin.view_services'))
    return render_template("admin/add_edit_view_services.html",form=form)

@admin.route("/services/editorview/<int:service_id>",methods=["GET", "POST"])
@login_required
@admin_required
def view_edit_services(service_id):
    servicedata = Services.query.filter(Services.id == service_id).first()
    if not servicedata or servicedata ==None:
        flash("Service NOT found","error")
        return redirect(url_for("admin.view_services"))
    form = ServiceForm()
    if form.validate_on_submit():
        service = Services.query.filter(Services.id == service_id).first()
        service.title = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.duration = form.duration.data
        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('admin.view_services'))
    return render_template("admin/add_edit_view_services.html",form=form,service=servicedata)


@admin.route("/services/delete/<int:service_id>",methods=["GET"])
@login_required
@admin_required
def deleteservice(service_id):
    serviceid = Services.query.filter(Services.id == service_id).first()
    if serviceid and not serviceid == None:
        db.session.delete(serviceid)
        db.session.commit()
        flash("Service Deleted","success")
    else:
        flash("Sorry DataNot Found","error")
    return redirect(url_for("admin.view_services"))
    

@admin.route("/view_booking")
@login_required
@admin_required
def view_booking():
    return render_template("admin/viewbooking.html")


@admin.route("/clients/view",methods=["GET"])
@login_required
@admin_required
def view_clients():
    userid = request.args.get('userid')
    typeof = "client"
    page = request.args.get('page', 1, type=int)
    if userid and userid!=None:
        users_data = Clients.query.filter(Clients.id == userid).first_or_404()
        return render_template("admin/view_user.html",user=users_data)
    users_data = Clients.query.paginate(page=page,per_page=10,error_out=False)
    return render_template("admin/viewusers.html",users=users_data,typeof=typeof)
        
@admin.route("/users/view",methods=["GET"])
@login_required
@admin_required
def view_users():
    userid = request.args.get('userid')
    typeof = 'user'
    page = request.args.get('page', 1, type=int)
    if userid and userid!=None:
        users_data = Users.query.filter(Users.id == userid).first_or_404()
        return render_template("admin/view_user.html",user=users_data)
    users_data = Users.query.paginate(page=page,per_page=10,error_out=False)
    return render_template("admin/viewusers.html",users=users_data,typeof=typeof)

@admin.route("/user/delete/<int:id>")
@admin_required
def deleteuser(id):
    userid = Users.query.get_or_404(id)
    bookings = Bookings.query.filter(Bookings.user_id == id).all()
    for booking in bookings:
        db.session.delete(booking)
    db.session.delete(userid)
    db.session.commit()
    flash("User Deleted","success")
    return redirect(url_for("admin.view_users"))

@admin.route("/client/delete/<int:id>")
@admin_required
def deleteclient(id):
    userid = Clients.query.get_or_404(id)
    bookings = Bookings.query.filter(
        (Bookings.client_id == id) | (Bookings.user_id == id)
    ).all()
    for booking in bookings:
        db.session.delete(booking)
    db.session.delete(userid)
    db.session.commit()
    flash("Client Deleted","success")
    return redirect(url_for("admin.view_clients"))
