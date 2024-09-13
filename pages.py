from flask import (
Blueprint, render_template, redirect, render_template, request,url_for,flash
)
from flask_login import current_user
from dbase import db
from models import ContactUs,Services
pages = Blueprint('pages', __name__)

@pages.route("/")
def home():
    servicesdata=Services.query.all()
    return render_template("pages/homepage.html",services=servicesdata)

@pages.route("/about")
def about():
    return render_template("pages/about.html")

@pages.route("/contact")
def contact():
    return render_template("pages/contact.html")

@pages.route("/services")
def services():
    servicesdata=Services.query.all()
    return render_template("pages/services.html",services=servicesdata)

@pages.route("/contactsubmit", methods=["GET", "POST"])
def contactsubmit():
    # try:
        if request.method == "POST":
            # from dbase import ContactUs,db
            if current_user.is_authenticated:
                try:
                    name = current_user.admin_name
                    phone_number = current_user.admin_phone_number
                except:
                    name = current_user.user_name
                    phone_number = current_user.user_phone_number
            else:
                name = request.form["name"]
                phone_number = request.form["phone"]
            service = request.form["service"]
            message = request.form["message"]
            if not name=="" and not phone_number=="" and not service=="" and not message=="":
                if len(message)>1000:
                    flash("Message Cant br more than 1000 charactors","success")
                    return redirect(url_for("pages.home"))
                contactsubmitvalue = ContactUs(name=name,phone_number=phone_number,service=service,message=message)
                db.session.add(contactsubmitvalue)
                db.session.commit()
                flash("Successfully Message Sent,will call back as as soon as possible!!","success")
                return redirect(url_for("pages.home"))
            else:
                flash("ERROR,Please enter the valid details, details cant be empty!!","error")
                return redirect(url_for("pages.home"))
        flash("ERROR,you cant access the page!!","error")
        return redirect(url_for("pages.home"))
    # except Exception as err:
    #     abort(404)
