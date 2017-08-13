import datetime

from werkzeug.security import generate_password_hash, \
    check_password_hash

from flask import Flask, request, redirect, url_for, flash, \
    render_template, g, session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

KEY_USERID = 'userid'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1@127.0.0.1:3306/testapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text)

    created_at = db.Column(db.DateTime,
        default=datetime.datetime.now)

    updated_at = db.Column(db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)


@app.before_request
def before_first_request():
    db.create_all()


@app.before_request
def before_request():
    g.user = None
    user_id = session.get(KEY_USERID)
    if user_id is not None:
        g.user = User.query.filter_by(id=user_id).first()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username:
            flash('username required')
            return redirect(url_for('signup'))

        if not email:
            flash('email required')
            return redirect(url_for('signup'))

        if not password:
            flash('password required')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('passwords did not match')
            return redirect(url_for('signup'))

        user = User(username=username,
            email=email,
            password=generate_password_hash(password))
        
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError as error:
            print(error.detail)
            print(error.args)
            print(error.message)
            flash('you have already registered')
            return redirect(url_for('signup'))

        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username,).first()

        if user is not None and \
            check_password_hash(user.password, password):
            session[KEY_USERID] = user.id
            return redirect(url_for('home'))

        flash('invalid username/password')
        return redirect(url_for('signin'))

    return render_template('signin.html')


@app.route('/signout', methods=['GET'])
def signout():
    session.pop(KEY_USERID, None)
    return redirect(url_for('signin'))


@app.route('/')
def home():
    name = 'World'
    if g.user is not None:
        name = g.user.username

    return render_template('home.html',
        message='Hello, {}!'.format(name))


if __name__ == '__main__':
    app.run()
