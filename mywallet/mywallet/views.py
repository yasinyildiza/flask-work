"""Submodule to keep view definitions."""

from flask import session, g

from . import app, constants, decorators, models


@app.before_request
def before_request():
    """Prepare context for the request."""
    g.user = None
    user_id = session.get(constants.KEY_USERID, None)
    if user_id:
        g.user = models.User.query.filter(models.User.id == user_id).first()

    decorators.create_user_tracking_record()

@app.route('/')
def index():
    """Show index/welcome page."""
    return render_template('index.html')
