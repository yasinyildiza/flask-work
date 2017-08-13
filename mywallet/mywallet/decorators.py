"""Submodule to organize decorators"""

from functools import wraps
from flask import flash, g, request, redirect, url_for

from . import constants, models


def login_required(f):
    """login_required view decorator"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        """login_required view decorator wrapper"""
        if g.user is None:
            flash('You need to log in to see this page')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return wrapper


def create_user_tracking_record():
    """create a UserTracking record for current request context"""
    if g.user is None:
        user = models.User.query.filter(
            models.User.username==constants.ANONYMOUS_USERNAME).one()
        user_id = user.id
    else:
        user_id = g.user.id
    record = models.UserTracking(user_id=user_id,
                                 ip=request.remote_addr,
                                 url=request.url)
    models.db.session.add(record)
    models.db.session.commit()

def track_user(f):
    """track user browsing"""
    @wraps(f)
    def wrapper(*arg, **kwargs):
        """track_user view decorator wrapper"""
        create_user_tracking_record()
        return f(*args, **kwargs)
    return wrapper
