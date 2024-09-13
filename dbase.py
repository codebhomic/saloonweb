from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_login import LoginManager
from flask import session

db = SQLAlchemy()

from models import AdminUser,Users

admin_login_manager = LoginManager()
admin_login_manager.login_view = 'users.signin'
admin_login_manager.login_message_category="error"

@admin_login_manager.user_loader
def admin_load_user(user_id):
    if session.get('user_type') == 'admin':
        return AdminUser.query.get(int(user_id))
    else:
        return Users.query.get(int(user_id))