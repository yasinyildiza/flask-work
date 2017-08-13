import os
import unittest
import tempfile

from werkzeug import check_password_hash, generate_password_hash
from flask import url_for

import mywallet


class MyWalletTestCase(unittest.TestCase):

    URL_REGISTER = '/register'
    URL_LOGIN = '/login'
    URL_LOGOUT = '/logout'
    URL_INDEX = '/'

    TITLE_SIGNIN = 'Sign In'
    TITLE_SIGNUP = 'Sign Up'
    TITLE_INDEX = 'Hello, World!'

    TITLE_ANONYMOUS = 'Welcome to MyWallet'
    TITLE_USER = staticmethod(lambda username: 'Hi, {}'.format(username))

    def setUp(self):
        self.db_fd, db_fname = tempfile.mkstemp()
        db_uri = 'sqlite:///' + db_fname
        mywallet.app.config['DATABASE'] = db_fname
        mywallet.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        mywallet.app.config['SQLALCHEMY_ECHO'] = False
        mywallet.app.testing = True
        self.app = mywallet.app.test_client()
        with mywallet.app.app_context():
            mywallet.models.db.create_all()

        self.username = 'tusernamet'
        self.password = 'tpasswordt'
        self.password2 = 'tpasswordt'
        self.first_name = 'tfirst_namet'
        self.last_name = 'tlast_namet'
        self.email = 'temailt@email.com'

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(mywallet.app.config['DATABASE'])

    def create_user(self, username=None, password=None,
                    first_name=None, last_name=None, email=None):

        username = self.username if username is None else username
        password = self.password if password is None else password
        first_name = self.first_name if first_name is None else first_name
        last_name = self.last_name if last_name is None else last_name
        email = self.email if email is None else email

        user = mywallet.models.User(username=username,
                                    pw_hash=generate_password_hash(password),
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)

        with mywallet.app.app_context():
            mywallet.models.db.session.add(user)
            mywallet.models.db.session.commit()

        return user

    def register_user(self, username=None, password=None, password2=None,
                      first_name=None, last_name=None, email=None,
                      follow_redirects=True):
        username = self.username if username is None else username
        password = self.password if password is None else password
        password2 = self.password2 if password2 is None else password2
        first_name = self.first_name if first_name is None else first_name
        last_name = self.last_name if last_name is None else last_name
        email = self.email if email is None else email

        data = dict(username=username,
                    password=password,
                    password2=password2,
                    first_name=first_name,
                    last_name=last_name,
                    email=email)
        return self.app.post(self.URL_REGISTER,
                             data=data,
                             follow_redirects=follow_redirects)

    def login_user(self, username=None, password=None, follow_redirects=True):
        username = self.username if username is None else username
        password = self.password if password is None else password

        data = dict(username=username,
                    password=password)
        return self.app.post(self.URL_LOGIN,
                             data=data,
                             follow_redirects=follow_redirects)

    def logout_user(self, follow_redirects=True):
        return self.app.get(self.URL_LOGOUT,
                            follow_redirects=follow_redirects)

    def test_register_get(self):
        rv = self.app.get(self.URL_REGISTER)
        self.assertIn(self.TITLE_SIGNUP, rv.data)
        self.assertNotIn(self.TITLE_SIGNIN, rv.data)

    def test_register_after_login(self):
        self.create_user()
        self.login_user()
        rv = self.register_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertNotIn(self.TITLE_ANONYMOUS, rv.data)
        self.assertIn(self.username, rv.data)

    def xtest_register_post_form_missing_field(self, field):
        data = dict(username=self.username,
                    password=self.password,
                    password2=self.password2,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email)
        del data[field]
        rv = self.app.post(self.URL_REGISTER, data=data)
        self.assertIn(self.TITLE_SIGNUP, rv.data)
        self.assertNotIn(self.TITLE_SIGNIN, rv.data)
        with mywallet.app.app_context():
            self.assertEqual(mywallet.models.User.query.count(), 0)
        return data, rv

    def test_register_post_form_missing_field(self):
        self.xtest_register_post_form_missing_field('username')
        self.xtest_register_post_form_missing_field('password')
        self.xtest_register_post_form_missing_field('password2')
        self.xtest_register_post_form_missing_field('first_name')
        self.xtest_register_post_form_missing_field('last_name')
        self.xtest_register_post_form_missing_field('email')

    def test_register_post_form_email_invalid(self):
        rv = self.register_user(email='invalid_email')
        self.assertIn(self.TITLE_SIGNUP, rv.data)
        self.assertNotIn(self.TITLE_SIGNIN, rv.data)
        with mywallet.app.app_context():
            self.assertEqual(mywallet.models.User.query.count(), 0)

    def test_register_post_password_mismatch(self):
        password2 = self.password2 * 2
        rv = self.register_user(password2=password2)
        self.assertIn(self.TITLE_SIGNUP, rv.data)
        self.assertNotIn(self.TITLE_SIGNIN, rv.data)
        with mywallet.app.app_context():
            self.assertEqual(mywallet.models.User.query.count(), 0)

    def test_register_post_username_taken(self):
        self.create_user()
        rv = self.register_user()
        self.assertIn(self.TITLE_SIGNUP, rv.data)
        self.assertNotIn(self.TITLE_SIGNIN, rv.data)
        with mywallet.app.app_context():
            self.assertEqual(mywallet.models.User.query.count(), 1)
            user = mywallet.models.User.query.all()[0]
            self.assertEqual(user.username, self.username)
            check_password_hash(user.pw_hash, self.password)
            self.assertEqual(user.first_name, self.first_name)
            self.assertEqual(user.last_name, self.last_name)
            self.assertEqual(user.email, self.email)

    def test_register_post_success(self):
        rv = self.register_user()
        self.assertNotIn(self.TITLE_SIGNUP, rv.data)
        self.assertIn(self.TITLE_SIGNIN, rv.data)
        with mywallet.app.app_context():
            self.assertEqual(mywallet.models.User.query.count(), 1)
            user = mywallet.models.User.query.all()[0]
            self.assertEqual(user.username, self.username)
            check_password_hash(user.pw_hash, self.password)
            self.assertEqual(user.first_name, self.first_name)
            self.assertEqual(user.last_name, self.last_name)
            self.assertEqual(user.email, self.email)

    def test_login_get(self):
        rv = self.app.get(self.URL_LOGIN)
        self.assertIn(self.TITLE_SIGNIN, rv.data)

    def test_login_after_login(self):
        self.create_user()
        self.login_user()
        rv = self.login_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_USER(self.username), rv.data)

    def xtest_login_post_form_missing_field(self, field):
        data = dict(username=self.username,
                    password=self.password)
        del data[field]
        rv = self.app.post(self.URL_LOGIN, data=data)
        self.assertIn(self.TITLE_SIGNIN, rv.data)
        return data, rv

    def test_login_post_form_missing_field(self):
        self.xtest_login_post_form_missing_field('username')
        self.xtest_login_post_form_missing_field('password')

    def test_login_post_username_invalid(self):
        rv = self.login_user()
        self.assertIn(self.TITLE_SIGNIN, rv.data)

    def test_login_post_password_mismatch(self):
        password = self.password * 2
        self.create_user()
        rv = self.login_user(password=password)
        self.assertIn(self.TITLE_SIGNIN, rv.data)

    def test_login_post_successful(self):
        self.create_user()
        rv = self.login_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_USER(self.username), rv.data)

    def test_logout_without_login(self):
        rv = self.logout_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_ANONYMOUS, rv.data)

    def test_logout(self):
        self.create_user()
        rv = self.login_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_USER(self.username), rv.data)
        rv = self.logout_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_ANONYMOUS, rv.data)

    def test_index_anonymous_user(self):
        rv = self.app.get(self.URL_INDEX)
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_ANONYMOUS, rv.data)

    def test_index_logged_in_user(self):
        self.create_user()
        rv = self.login_user()
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_USER(self.username), rv.data)
        rv = self.app.get(self.URL_INDEX)
        self.assertIn(self.TITLE_INDEX, rv.data)
        self.assertIn(self.TITLE_USER(self.username), rv.data)
