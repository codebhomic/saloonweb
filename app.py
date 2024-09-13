from flask import (
    Flask, flash, redirect, render_template, request, session, url_for,abort
)
from dbase import db,admin_login_manager
from models import *
from pages import pages
from admin import admin
from auth import auth
from users import users
from booking import booking
import os



app = Flask(__name__)
app.register_blueprint(pages)
app.register_blueprint(admin)
app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(booking)

@app.errorhandler(404)
def page_404(error):
    return render_template('404.html'), 404

app.secret_key = 'your_secret_key'
app.secret_key = 'your_secret_key_1'
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///appdatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
admin_login_manager.init_app(app)
# main routing for our app

# routing for database related
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)
    if (not os.path.exists("instance/appdatabase.db")):
        session.clear()
    # app.run(debug=True,host=local_ip)