"""populate database with dummy record for manual testing"""

from werkzeug import generate_password_hash

from mywallet import app, models


@app.cli.command()
def populatedb():  # pragma no cover
    """Populate the database."""
    user = models.User(username="user",
                       pw_hash=generate_password_hash("1"),
                       first_name="First",
                       last_name="Last",
                       email="user@mywallet.com")
    models.db.session.add(user)

    for i in range(3):
        category = models.Category(code=i,
                                   name="Category{}".format(i+1),
                                   description="Desc{}".format(i+1))
        models.db.session.add(category)

    for i in range(5):
        tag = models.Tag(name="Tag{}".format(i+1),
                         description="Desc{}".format(i+1))
        models.db.session.add(tag)
        
    models.db.session.commit()
