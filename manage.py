import os
from app import create_app, db
from app.models import User, Role, Follow, Like, Post
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

app = create_app('default')
migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def insert_roles_and_users():
    admin_role = Role(name='Administrator')
    mod_role = Role(name='Modetator')
    user_role = Role(name='User')
    user_susan = User(username='Susan', role=admin_role)
    user_join = User(username='Join', role=user_role)
    user_david = User(username='David', role=user_role)
    db.session.add_all([admin_role, mod_role, user_role, user_susan, user_join, user_david])
    db.session.commit()


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Follow=Follow, Like=Like, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
