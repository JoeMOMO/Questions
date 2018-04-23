from functools import wraps
from flask import session,redirect,url_for

def login_required(func):
    @wraps(func)
    def wrapper(*arg, **kw):
        if session.get('user_id'):
            return func(*arg, **kw)
        else:
            return redirect(url_for('login'))
    return wrapper