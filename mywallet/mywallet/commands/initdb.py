"""initialize database with tables define in models"""

from mywallet import app, models


@app.cli.command()
def initdb():  # pragma no cover
    """Initialize the database."""
    models.db.create_all()
