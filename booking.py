from flask import (
    Flask,Blueprint, flash, redirect, render_template, request, session, url_for,abort
)
from dbase import db
from flask_login import current_user,login_required
from models import Services,Bookings,Clients

booking = Blueprint('booking', __name__, url_prefix='/book')
import datetime
from pytz import timezone 
from forms import BookingForm


@booking.route('/', methods=["GET", "POST"])
def bookingpage():
    service = Services.query.all()
    form = BookingForm()
    if form.validate_on_submit():
        from datetime import datetime
        time_str = form.time.data
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        service_id=request.form['service_id']
        if current_user.is_authenticated:
            bookingsubmit = Bookings(
                user_id=current_user.id,
                service_id=service_id,
                date=form.date.data,time=time_obj,
                status="booked"
            )
            db.session.add(bookingsubmit)
            db.session.commit()
            flash("Your Booking is done, if you want to see live status please check email or create account with same details","success")
            return redirect(url_for("booking.bookingpage"))
        else:
            clientid=Clients.query.filter(Clients.email_address==form.email_address.data).first()
            if not clientid:
                client = Clients(name=form.name.data,email_address=form.email_address.data,phone_number=form.phone_number.data)
                db.session.add(client)
                db.session.commit()
            clientid=Clients.query.filter(Clients.email_address==form.email_address.data).first()
            if clientid:
                bookingsubmit = Bookings(
                client_id=clientid.id,
                service_id=request.form['service_id'],
                date=form.date.data,time=time_obj,
                status="booked"
                )
                db.session.add(bookingsubmit)
                db.session.commit()
                flash("Your Booking is done, if you want to see live status please check email or create account with same details","success")
                return redirect(url_for("booking.bookingpage"))
            else:
                flash("some error occured","error")
                return redirect(url_for("booking.bookingpage"))
    return render_template('booking/booking_details.html',services=service,form=form)

@booking.route('<int:service_id>', methods=["GET", "POST"])
def bookingservice(service_id):
    service = Services.query.all()
    form = BookingForm()
    if form.validate_on_submit():
        from datetime import datetime
        time_str = form.time.data
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        if current_user.is_authenticated:
            bookingsubmit = Bookings(
                user_id=current_user.id,
                service_id=request.form['service_id'],
                date=form.date.data,time=time_obj,
                status="booked"
            )
            db.session.add(bookingsubmit)
            db.session.commit()
            flash("Your Booking is done, if you want to see live status please check email or create account with same details","success")
            return redirect(url_for("booking.bookingservice",service_id=service_id))
        else:
            clientid=Clients.query.filter(Clients.email_address==form.email_address.data).first()
            if not clientid:
                client = Clients(name=form.name.data,email_address=form.email_address.data,phone_number=form.phone_number.data)
                db.session.add(client)
                db.session.commit()
            clientid=Clients.query.filter(Clients.email_address==form.email_address.data).first()
            if clientid:
                bookingsubmit = Bookings(
                client_id=clientid.id,
                service_id=request.form['service_id'],
                date=form.date.data,time=time_obj,
                status="booked"
                )
                db.session.add(bookingsubmit)
                db.session.commit()
                flash("Your Booking is done, if you want to see live status please check email or create account with same details","success")
                return redirect(url_for("booking.bookingservice",service_id=service_id))
            else:
                flash("some error occured","error")
                return redirect(url_for("booking.bookingservice",service_id=service_id))

    return render_template('booking/booking_details.html',services=service,id=service_id,form=form)

@booking.route('/info')
@login_required
def booking_info():
    bookinginfo = Bookings.query.filter(Bookings.user_id==current_user.id).all()
    services = Services.query.all()
    return render_template('booking/booking_info.html',binfo=bookinginfo,serv=services)