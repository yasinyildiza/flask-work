"""Create a dummy user to be used for anonymous visits"""

from mywallet import app, constants, models


@app.cli.command()
def createanonymoususer():  # pragma no cover
    """Create an anonymous user."""
    user = models.User(username=constants.ANONYMOUS_USERNAME,
                       pw_hash='',
                       first_name='',
                       last_name='',
                       email='',
                       is_active=False,
                       is_admin=False)
    models.db.session.add(user)        
    models.db.session.commit()
