"""Category Blueprint for CRUD views"""

from flask import Blueprint, request, session, url_for, redirect, \
    render_template, g, flash

from mywallet import models
from mywallet.decorators import login_required
from mywallet.forms.category import CategoryForm

bp = Blueprint('category', __name__, template_folder='templates')


@bp.route('/index', methods=['GET'])
@login_required
def index():
    """List all categories."""
    records = models.Category.query.all()
    return render_template('category/index.html',
                           modelname=models.Category.plural,
                           records=records)


@bp.route('/create', defaults={'id': None}, methods=['GET', 'POST'])
@bp.route('/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create(id=None):
    """Create a new category."""
    title = 'New'
    record = models.Category()
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(record)
        models.db.session.add(record)
        models.db.session.commit()
        flash('Record created')
        return redirect(url_for('category.show', id=record.id))

    return render_template('category/form.html',
                           title=title,
                           modelname=models.Category.singular,
                           form=form,
                           record=record)


@bp.route('/update', defaults={'id': None}, methods=['GET', 'POST'])
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id=None):
    """Update an existing one."""
    title = 'Edit'
    record = models.Category.query.get_or_404(id)
    form = CategoryForm(request.form, obj=record)
    if request.method == 'POST' and form.validate():
        form.populate_obj(record)
        models.db.session.commit()
        flash('Record updated')
        return redirect(url_for('category.show', id=record.id))

    return render_template('category/form.html',
                           title=title,
                           modelname=models.Category.singular,
                           form=form,
                           record=record)


@bp.route('/show/<int:id>', methods=['GET'])
@login_required
def show(id):
    """Show details of a category."""
    record = models.Category.query.get_or_404(id)
    return render_template('category/show.html',
                           modelname=models.Category.singular,
                           record=record)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete a category."""
    record = models.Category.query.get_or_404(id)
    models.db.session.delete(record)
    models.db.session.commit()
    flash('Record deleted')
    return redirect(url_for('category.index'))
