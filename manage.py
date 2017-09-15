#!/usr/bin/env python
import os
from app.app import create_app
from app.extensions import db
from app.models import User, Post, Category, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Category=Category, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
	"""Run deployment tasks"""
	from flask_migrate import upgrade
	from app.models import Role, User, Post, Category

	#migrate to latest revision
	upgrade()

	#create user roles
	Role.insert_roles()



if __name__ == '__main__':
    manager.run()