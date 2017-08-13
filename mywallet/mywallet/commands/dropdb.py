"""Drop database"""

from mywallet import app, models


@app.cli.command()
def dropdb():  # pragma no cover
    """Drop the database."""
    models.db.drop_all()
