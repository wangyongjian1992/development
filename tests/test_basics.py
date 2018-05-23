import unittest
from flask import current_app
from app import create_app, db
from app.models import User, Permissions, Role

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_generate_register_token(self):
        u = User(id=3, username='cat', email='aa@aa.com')
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
        self.assertTrue(u.confirmed)

    def test_generate_reset_token(self):
        u = User(username='cat', email='aa@aa.com')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'newpassword'))
        self.assertTrue(u.verify_password('newpassword'))

    def test_permissions(self):
        Role.insert_roles()
        u1 = User(username='cat', email='yongjianw_92@163.com')
        u2 = User(username='sog', email='aa@aa.com')
        self.assertTrue(u1.is_administrator())
        self.assertTrue(u1.can(Permissions.MODERATE_COMMENTS))
        self.assertFalse(u2.is_administrator())
        self.assertFalse(u2.can(Permissions.ADMINISTER))
