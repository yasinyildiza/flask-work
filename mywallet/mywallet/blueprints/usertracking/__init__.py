"""UserTracking Blueprint for CRUD views"""

from flask import Blueprint, request, session, url_for, redirect, \
    render_template, g, flash

from mywallet import models
from mywallet.decorators import login_required

bp = Blueprint('usertracking', __name__, template_folder='templates')


@bp.route('/index', methods=['GET'])
@login_required
def index():
    """List all usertrackings."""
    records = models.UserTracking.query.all()
    return render_template('usertracking/index.html',
                           modelname=models.UserTracking.plural,
                           records=records)


@bp.route('/show/<int:id>', methods=['GET'])
@login_required
def show(id):
    """Show details of a usertracking."""
    record = models.UserTracking.query.get_or_404(id)
    return render_template('usertracking/show.html',
                           modelname=models.UserTracking.singular,
                           record=record)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete a usertracking."""
    record = models.UserTracking.query.get_or_404(id)
    models.db.session.delete(record)
    models.db.session.commit()
    flash('Record deleted')
    return redirect(url_for('usertracking.index'))
