"""MyWallet Flask app"""

from mywalletapp import create_app

# Flask app instance
app = create_app()

# import submodules
from . import blueprints, commands, decorators, forms, models, views
