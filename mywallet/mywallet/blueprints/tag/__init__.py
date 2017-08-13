"""Tag Blueprint for CRUD views"""

from flask import Blueprint, request, session, url_for, redirect, \
    render_template, g, flash

from mywallet import models
from mywallet.decorators import login_required
from mywallet.forms.tag import TagForm

bp = Blueprint('tag', __name__, template_folder='templates')


@bp.route('/index', methods=['GET'])
@login_required
def index():
    """List all tags."""
    records = models.Tag.query.all()
    return render_template('tag/index.html',
                           modelname=models.Tag.plural,
                           records=records)


@bp.route('/create', defaults={'id': None}, methods=['GET', 'POST'])
@bp.route('/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create(id=None):
    """Create a new tag."""
    title = 'New'
    record = models.Tag()
    form = TagForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(record)
        models.db.session.add(record)
        models.db.session.commit()
        flash('Record created')
        return redirect(url_for('tag.show', id=record.id))

    return render_template('tag/form.html',
                           title=title,
                           modelname=models.Tag.singular,
                           form=form,
                           record=record)


@bp.route('/update', defaults={'id': None}, methods=['GET', 'POST'])
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id=None):
    """Update an existing one."""
    title = 'Edit'
    record = models.Tag.query.get_or_404(id)
    form = TagForm(request.form, obj=record)
    if request.method == 'POST' and form.validate():
        form.populate_obj(record)
        models.db.session.commit()
        flash('Record updated')
        return redirect(url_for('tag.show', id=record.id))

    return render_template('tag/form.html',
                           title=title,
                           modelname=models.Tag.singular,
                           form=form,
                           record=record)


@bp.route('/show/<int:id>', methods=['GET'])
@login_required
def show(id):
    """Show details of a tag."""
    record = models.Tag.query.get_or_404(id)
    return render_template('tag/show.html',
                           modelname=models.Tag.singular,
                           record=record)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete a tag."""
    record = models.Tag.query.get_or_404(id)
    models.db.session.delete(record)
    models.db.session.commit()
    flash('Record deleted')
    return redirect(url_for('tag.index'))
