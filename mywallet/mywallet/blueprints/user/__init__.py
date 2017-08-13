"""User Blueprint for CRUD views"""

from flask import Blueprint, request, session, url_for, redirect, \
    render_template, g, flash
from werkzeug import check_password_hash, \
    generate_password_hash

from mywallet import constants, models
from mywallet.decorators import login_required
from mywallet.forms.user import LoginForm, RegistrationForm, UserForm

bp = Blueprint('user', __name__, template_folder='templates')


@bp.route('/index', methods=['GET'])
@login_required
def index():
    """List all users."""
    records = models.User.query.all()
    return render_template('user/index.html',
                           modelname=models.User.plural,
                           records=records,
                           guser=g.user)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Registers the user."""
    if g.user:
        return redirect(url_for('index'))

    error = None
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.password.data == form.password2.data:
            if models.User.query.filter(
                    models.User.username == form.username.data).count() == 0:
                user = models.User(username=form.username.data,
                                   pw_hash=generate_password_hash(form.password.data),
                                   first_name=form.first_name.data,
                                   last_name=form.last_name.data,
                                   email=form.email.data)

                models.db.session.add(user)
                models.db.session.commit()

                flash('You were successfully registered and can login now')

                return redirect(url_for('login'))
            else:
                error = 'Username already taken'
        else:
            error = 'Passwords did not match'

    if error:
        flash(error)

    return render_template('user/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('index'))

    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = models.User.query.filter(models.User.username == form.username.data).first()

        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.pw_hash, form.password.data):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session[constants.KEY_USERID] = user.id
            return redirect(url_for('index'))

    if error:
        flash(error)

    return render_template('user/login.html', form=form)


@bp.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')

    session.pop(constants.KEY_USERID, None)

    return redirect(url_for('index'))

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update(id=None):
    """Update user profile."""
    record = g.user
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.password.data == form.password2.data:
            if form.password.data:
                record.pw_hash = generate_password_hash(form.password.data)
            record.first_name = form.first_name.data
            record.last_name = form.last_name.data
            record.email = form.email.data
            models.db.session.commit()

            flash('Your profile updated')
            return redirect(url_for('user.show', id=record.id))

    return render_template('user/profileform.html',
                           form=form,
                           record=record)


@bp.route('/show/<int:id>', methods=['GET'])
@login_required
def show(id):
    """Show details of a user."""
    record = models.User.query.get_or_404(id)
    return render_template('user/show.html',
                           modelname=models.User.singular,
                           record=record,
                           guser=g.user)


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    """Delete a user."""
    record = g.user
    models.db.session.delete(record)
    models.db.session.commit()
    flash('Your account deleted')
    return redirect(url_for('index'))
