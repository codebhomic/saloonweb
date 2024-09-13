from dbase import db
from flask_login import UserMixin
import datetime
from pytz import timezone 

# declaring tables for our app
class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(500), nullable=False, default=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))
    
    def __repr__(self):
        return f'<Name: {self.username}, Phone Number: {self.phone_number}, Services: {self.service}, Messages: {self.message}>'

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.String(500), nullable=False, default=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))
    
    def __repr__(self):
        return f'<Name: {self.name}, email_address: {self.email_address}, Phone Number: {self.phone_number}, date_created: {self.date_created}>'

class AdminUser(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_phone_number = db.Column(db.Integer, nullable=False,unique=True)
    admin_email_address = db.Column(db.String(100), nullable=False,unique=True)
    admin_password = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(500), nullable=False, default=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))
    
    def __repr__(self):
        return f'<Admin Name: {self.admin_name}, admin_email_address: {self.admin_email_address}>'

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    user_name = db.Column(db.String(100), nullable=False,unique=True)
    user_phone_number = db.Column(db.Integer, nullable=False,unique=True)
    user_email_address = db.Column(db.String(100), nullable=False,unique=True)
    user_password = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(500), nullable=False, default=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))

    def __repr__(self):
        return f'<User Name: {self.user_name}, email_address: {self.user_email_address}>'

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.String(500), nullable=False, default=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))
    
    def __repr__(self):
        return f'<title: {self.title}, desc: {self.desc}, price: {self.price}, duration: {self.duration}, date_created: {self.date_created}>'

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    # desc = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False)  # 'reject','booked', 'completed', 'cancelled', etc.
    users = db.relationship('Users', backref=db.backref('bookings', lazy=True))
    clients = db.relationship('Clients', backref=db.backref('bookings', lazy=True))
    services = db.relationship('Services', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<user_id: {self.user_id}, client_id: {self.client_id}, service_id: {self.service_id}, date: {self.date}, time: {self.time}, status: {self.status}>'

class CategoryArticles(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(100))
    label = db.Column(db.String(100))
    tags = db.Column(db.String(100))
    slug = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.String(500), nullable=False, default=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))
    
    def __repr__(self):
        return f'<title: {self.title}, desc: {self.desc}, price: {self.price}, duration: {self.duration}, date_created: {self.date_created}>'
