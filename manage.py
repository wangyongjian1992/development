import os
import redis
from app import create_app, db
from app.models import User, Role, Follow, Like, Post
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell


app = create_app('default')
migrate = Migrate(app, db)
manager = Manager(app)
redis_conn = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

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
